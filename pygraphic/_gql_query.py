from __future__ import annotations

from typing import Iterator, Optional

import pydantic

from ._gql_parameters import GQLParameters
from ._gql_type import GQLType
from .types import class_to_graphql_type


class GQLQuery(GQLType):
    @classmethod
    def get_query_string(cls, named: bool = True) -> str:
        parameters: Optional[
            type[GQLParameters]
        ] = cls.__config__.parameters  # type: ignore

        if not named and parameters is not None:
            # TODO Find a better exception type
            raise Exception("Query with parameters must have a name")

        def _gen():
            if named:
                params = "".join(_gen_parameter_string(parameters))
                yield "query " + cls.__name__ + params + " {"
            else:
                yield "query {"
            for line in cls.generate_query_lines(nest_level=1):
                yield line
            yield "}"

        return "\n".join(_gen())

    class Config(pydantic.BaseConfig):
        parameters: Optional[type[GQLParameters]] = None


def _gen_parameter_string(parameters: Optional[type[GQLParameters]]) -> Iterator[str]:
    if parameters is None or not parameters.__fields__:
        return
    yield "("
    for field in parameters.__fields__.values():
        yield "$"
        yield field.alias
        yield ": "
        yield class_to_graphql_type(field.type_, allow_none=field.allow_none)
    yield ")"
