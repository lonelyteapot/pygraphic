import inspect
import json
import typing
from enum import Enum
from types import UnionType
from typing import Any, Iterator

import pydantic
from pydantic.fields import ModelField

from .defaults import default_alias_generator


class GQLType(pydantic.BaseModel):
    @classmethod
    def generate_query_lines(cls, nest_level: int = 0) -> Iterator[str]:
        fields = typing.get_type_hints(cls)
        for field_name, field_type in fields.items():
            field = cls.__fields__[field_name]
            arguments_str = _get_arguments_string(field.field_info.extra)
            if typing.get_origin(field_type) is list:
                args = typing.get_args(field_type)
                assert len(args) == 1
                field_type = args[0]
            if typing.get_origin(field_type) is UnionType:
                sub_types = typing.get_args(field_type)
                yield "  " * nest_level + field.alias + arguments_str + " {"
                for sub_type in sub_types:
                    if sub_type is object:
                        continue
                    assert issubclass(sub_type, GQLType)
                    yield "  " * (nest_level + 1) + "... on " + sub_type.__name__ + " {"
                    for line in sub_type.generate_query_lines(
                        nest_level=nest_level + 2
                    ):
                        yield line
                    yield "  " * (nest_level + 1) + "}"
                yield "  " * nest_level + "}"
                continue
            if not inspect.isclass(field_type):
                raise Exception(f"Type {field_type} not supported")
            if issubclass(field_type, GQLType):
                field_type.update_forward_refs()
                yield "  " * nest_level + field.alias + arguments_str + " {"
                for line in field_type.generate_query_lines(nest_level=nest_level + 1):
                    yield line
                yield "  " * nest_level + "}"
                continue
            yield "  " * nest_level + field.alias + arguments_str
            continue

    class Config:
        alias_generator = default_alias_generator
        allow_population_by_field_name = True


def _get_arguments_string(arguments: dict[str, Any]) -> str:
    if not arguments:
        return ""

    def _serialize_value(value: Any) -> str:
        if type(value) is ModelField:
            return "$" + value.alias
        if isinstance(value, Enum):
            return value.name
        return json.dumps(value, indent=None, default=str)

    def _generate():
        for name, value in arguments.items():
            yield default_alias_generator(name) + ": " + _serialize_value(value)

    return "(" + ", ".join(_generate()) + ")"
