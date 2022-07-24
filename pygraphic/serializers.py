import json
from enum import Enum
from typing import Any

import inflection
from pydantic.fields import ModelField


_class_mapping: dict[type, str] = {
    int: "Int",
    float: "Float",
    str: "String",
    bool: "Boolean",
}


def register_graphql_type(graphql_type: str, python_class: type) -> None:
    _class_mapping[python_class] = graphql_type


def class_to_graphql(cls: type, allow_none: bool) -> str:
    suffix = "" if allow_none else "!"
    if issubclass(cls, Enum):
        return cls.__name__ + suffix
    try:
        type_ = _class_mapping[cls]
        return type_ + suffix
    except KeyError:
        raise TypeError(
            f"Type '{cls}' could not be converted to a GraphQL type."
            "See pygraphic.types.register_graphql_type"
        )


def value_to_graphql(value: Any) -> str:
    if type(value) is ModelField:
        return "$" + value.alias
    if isinstance(value, Enum):
        return value.name
    return json.dumps(value, indent=None, default=str)


def key_to_graphql(key: str) -> str:
    return inflection.camelize(key, uppercase_first_letter=False)
