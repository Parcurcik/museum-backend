from typing import Literal, TypeVar, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import ModelField

_BaseModelT = TypeVar('_BaseModelT', bound=BaseModel)


def with_literal_default(cls: _BaseModelT) -> _BaseModelT:
    for model_field in cls.__fields__.values():
        model_field: ModelField
        if get_origin(model_field.type_) is Literal and model_field.default is None:
            default = get_args(model_field.type_)[0]
            model_field.field_info.default = default
            model_field.default = default
            model_field.required = False
    return cls
