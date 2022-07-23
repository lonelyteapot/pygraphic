from typing import Optional

import pydantic

from ._gql_type import GQLType
from ._gql_variables import GQLVariables
from .exceptions import QueryGenerationError
from .types import class_to_graphql_type


class GQLQuery(GQLType):
    @classmethod
    def get_query_string(cls, include_name: bool = True) -> str:
        variables: Optional[
            type[GQLVariables]
        ] = cls.__config__.variables  # type: ignore

        if variables and not include_name:
            raise QueryGenerationError("Query with variables must include a name")

        def _generate():
            if include_name:
                variables_str = _get_variables_string(variables)
                yield "query " + cls.__name__ + variables_str + " {"
            else:
                yield "query {"
            for line in cls.generate_query_lines():
                yield "  " + line
            yield "}"

        return "\n".join(_generate())

    class Config(pydantic.BaseConfig):
        variables: Optional[type[GQLVariables]] = None


def _get_variables_string(variables: Optional[type[GQLVariables]]) -> str:
    if variables is None or not variables.__fields__:
        return ""

    def _generate():
        for field in variables.__fields__.values():
            yield "$" + field.alias + ": " + class_to_graphql_type(
                field.type_, allow_none=field.allow_none
            )

    return "(" + ", ".join(_generate()) + ")"
