import inspect
import json
import typing
from typing import Any, Iterator

import pydantic
from pydantic.fields import ModelField


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
            field_extra = cls.__fields__[field_name].field_info.extra
            params = "".join(_gen_parameter_string(field_extra))
            if issubclass(field_type, GQLType):
                field_type.update_forward_refs()
                yield "  " * nest_level + field_name + params + " {"
                for line in field_type.generate_query_lines(nest_level=nest_level + 1):
                    yield line
                yield "  " * nest_level + "}"
                continue
            yield "  " * nest_level + field_name + params
            continue


def _gen_parameter_string(parameters: dict[str, Any]) -> Iterator[str]:
    if not parameters:
        return
    yield "("
    for name, value in parameters.items():
        yield name
        yield ": "
        if type(value) is ModelField:
            yield "$" + value.name
            continue
        yield json.dumps(value, indent=None, default=str)
    yield ")"
