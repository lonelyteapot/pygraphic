from __future__ import annotations

from typing import Any

import pydantic
import pydantic.main

from .defaults import default_alias_generator


class ModelMetaclass(pydantic.main.ModelMetaclass):
    def __getattr__(cls, __name: str) -> Any:
        try:
            return cls.__fields__[__name]
        except KeyError:
            raise AttributeError(
                f"type object '{cls.__name__}' has no attribute '{__name}'"
            )


class GQLParameters(
    pydantic.BaseModel,
    metaclass=ModelMetaclass,
    alias_generator=default_alias_generator,
    allow_population_by_field_name=True,
):
    def json(self, **kwargs: Any) -> str:
        return super().json(by_alias=True, **kwargs)
