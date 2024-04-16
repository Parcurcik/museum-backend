from __future__ import annotations

from typing import Any, Type

from pydantic import BaseModel as BaseModel_

from api.utils.types import DictStrAny


class BaseModel(BaseModel_):
    def dict(self, *args: Any, **kwargs: Any) -> DictStrAny:
        if 'exclude_unset' not in kwargs:
            kwargs['exclude_unset'] = True
        return super().dict(*args, **kwargs)

    class Config(BaseModel_.Config):
        @staticmethod
        def schema_extra(schema: DictStrAny, model: Type[BaseModel]) -> None:
            schema['properties'] = {
                k: v for k, v in schema.get('properties', {}).items() if not model.__fields__[k].field_info.exclude
            }


class TrimModel(BaseModel):
    class Config(BaseModel.Config):
        anystr_strip_whitespace = True
