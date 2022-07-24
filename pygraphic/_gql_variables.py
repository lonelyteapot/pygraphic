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
            mcs: type[GQLVariables] = cls  # type: ignore
            return mcs.__fields__[__name]
        except KeyError:
            raise AttributeError(
                f"type object '{cls.__name__}' has no attribute '{__name}'"
            )


class GQLVariables(pydantic.BaseModel, metaclass=ModelMetaclass):
    def json(self, exclude_defaults: bool = True, **kwargs: Any) -> str:
        exclude = set[str]()
        if exclude_defaults:
            for field_name, field in self.__fields__.items():
                if (field_name in self.__fields_set__) or (not field.allow_none):
                    continue
                exclude.add(field_name)
        return super().json(by_alias=True, exclude=exclude, **kwargs)

    class Config:
        alias_generator = default_alias_generator
        allow_population_by_field_name = True
