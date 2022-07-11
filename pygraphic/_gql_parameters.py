from __future__ import annotations

from typing import Any

import pydantic
import pydantic.main


class ModelMetaclass(pydantic.main.ModelMetaclass):
    def __getattr__(cls, __name: str) -> Any:
        try:
            return cls.__fields__[__name]
        except KeyError:
            raise AttributeError(
                f"type object '{cls.__name__}' has no attribute '{__name}'"
            )


class GQLParameters(pydantic.BaseModel, metaclass=ModelMetaclass):
    def __str__(self):
        return ""
