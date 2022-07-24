from typing import Any

import pydantic
import pydantic.main
from pydantic.fields import Field, FieldInfo
from pydantic.main import __dataclass_transform__

from .serializers import key_to_graphql


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
    def _get_unset_defaults(self) -> set[str]:
        unset_defaults = set[str]()
        for field_name, field in self.__fields__.items():
            if (field_name in self.__fields_set__) or (not field.allow_none):
                continue
            unset_defaults.add(field_name)
        return unset_defaults

    def dict(
        self,
        by_alias: bool = True,
        exclude_defaults: bool = True,
        **kwargs: Any,
    ) -> dict[str, Any]:
        exclude = self._get_unset_defaults() if exclude_defaults else set()
        return super().dict(by_alias=by_alias, exclude=exclude, **kwargs)

    def json(
        self,
        by_alias: bool = True,
        exclude_defaults: bool = True,
        **kwargs: Any,
    ) -> str:
        exclude = self._get_unset_defaults() if exclude_defaults else set()
        return super().json(by_alias=by_alias, exclude=exclude, **kwargs)

    class Config:
        alias_generator = key_to_graphql
        allow_population_by_field_name = True
