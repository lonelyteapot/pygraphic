from typing import Optional

import pydantic
from pydantic.fields import Undefined

from ._gql_type import GQLType
from ._gql_variables import GQLVariables
from .serializers import class_to_graphql, value_to_graphql


class GQLQuery(GQLType):
    @classmethod
    def get_query_string(cls, include_name: bool = True) -> str:
        variables: Optional[
            type[GQLVariables]
        ] = cls.__config__.variables  # type: ignore

        def _generate():
            variables_str = _get_variables_string(variables)
            query_name = " " + cls.__name__ if include_name else ""
            yield "query" + query_name + variables_str + " {"
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
            type_str = class_to_graphql(field.type_, allow_none=field.allow_none)
            if field.allow_none and field.field_info.default is not Undefined:
                default_str = " = " + value_to_graphql(field.default)
            else:
                default_str = ""
            yield "$" + field.alias + ": " + type_str + default_str

    return "(" + ", ".join(_generate()) + ")"
