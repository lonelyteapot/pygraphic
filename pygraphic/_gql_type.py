import inspect
import json
import typing
from typing import Any, Iterator

import pydantic
from pydantic.fields import ModelField

from .defaults import default_alias_generator


class GQLType(pydantic.BaseModel):
    @classmethod
    def generate_query_lines(cls, nest_level: int = 0) -> Iterator[str]:
        fields = typing.get_type_hints(cls)
        for field_name, field_type in fields.items():
            if typing.get_origin(field_type) is list:
                args = typing.get_args(field_type)
                assert len(args) == 1
                field_type = args[0]
            if not inspect.isclass(field_type):
                raise Exception(f"Type {field_type} not supported")
            field = cls.__fields__[field_name]
            params = "".join(_gen_parameter_string(field.field_info.extra))
            if issubclass(field_type, GQLType):
                field_type.update_forward_refs()
                yield "  " * nest_level + field.alias + params + " {"
                for line in field_type.generate_query_lines(nest_level=nest_level + 1):
                    yield line
                yield "  " * nest_level + "}"
                continue
            yield "  " * nest_level + field.alias + params
            continue

    class Config:
        alias_generator = default_alias_generator
        allow_population_by_field_name = True


def _gen_parameter_string(parameters: dict[str, Any]) -> Iterator[str]:
    if not parameters:
        return
    yield "("
    for name, value in parameters.items():
        yield default_alias_generator(name)
        yield ": "
        if type(value) is ModelField:
            yield "$" + value.alias
            continue
        yield json.dumps(value, indent=None, default=str)
    yield ")"
