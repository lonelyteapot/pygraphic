from typing import Any, Iterator, Optional

from ._gql_parameters import GQLParameters
from ._gql_type import GQLType
from .defaults import default_alias_generator
from .types import class_to_graphql_type


class GQLQuery(
    GQLType,
    alias_generator=default_alias_generator,
    allow_population_by_field_name=True,
):
    __parameters__ = None

    @classmethod
    def get_query_string(cls, named: bool = True) -> str:
        if not named and cls.__parameters__ is not None:
            # TODO Find a better exception type
            raise Exception("Query with parameters must have a name")

        def _gen():
            if named:
                params = "".join(_gen_parameter_string(cls.__parameters__))
                yield "query " + cls.__name__ + params + " {"
            else:
                yield "query {"
            for line in cls.generate_query_lines(nest_level=1):
                yield line
            yield "}"

        return "\n".join(_gen())

    def __init_subclass__(
        cls,
        parameters: Optional[type[GQLParameters]] = None,
        **pydantic_kwargs: Any,
    ) -> None:
        cls.__parameters__ = parameters
        return super().__init_subclass__(**pydantic_kwargs)


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
