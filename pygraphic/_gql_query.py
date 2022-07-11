from typing import Any, Iterator, Optional

from ._gql_parameters import GQLParameters
from ._gql_type import GQLType
from .types import class_to_graphql_type


class GQLQuery(GQLType):
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
    for name, field in parameters.__fields__.items():
        yield "$"
        yield name
        yield ": "
        yield class_to_graphql_type(field.type_)
    yield ")"
