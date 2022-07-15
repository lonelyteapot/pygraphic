from __future__ import annotations

from typing import Any

import pydantic
import pydantic.main
from pydantic.fields import Field, FieldInfo
from pydantic.main import __dataclass_transform__

from .defaults import default_alias_generator


@__dataclass_transform__(kw_only_default=True, field_descriptors=(Field, FieldInfo))
class ModelMetaclass(pydantic.main.ModelMetaclass):
    def __getattr__(cls, __name: str) -> Any:
        try:
            mcs: type[GQLParameters] = cls  # type: ignore
            return mcs.__fields__[__name]
        except KeyError:
            raise AttributeError(
                f"type object '{cls.__name__}' has no attribute '{__name}'"
            )


class GQLParameters(pydantic.BaseModel, metaclass=ModelMetaclass):
    def json(self, **kwargs: Any) -> str:
        return super().json(by_alias=True, **kwargs)

    class Config:
        alias_generator = default_alias_generator
        allow_population_by_field_name = True
