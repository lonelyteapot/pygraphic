from enum import Enum
from typing import Any


class GQLEnum(Enum):
    @classmethod
    def validate(cls, value: Any) -> "GQLEnum":
        if isinstance(value, str):
            # Find Enum member by name
            try:
                return cls[value]
            except KeyError:
                pass
        return cls(value)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(enum=[member.name for member in cls])
