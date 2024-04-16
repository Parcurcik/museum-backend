from typing import List, Literal, Tuple

from pydantic import Field

from api.utils.error_codes import ErrorCode
from api.utils.schemas import with_literal_default
from api.utils.types import TupleStr
from .base import TrimModel

_ERROR_CODE_DESCRIPTION = 'The error code'


class BaseError(TrimModel):
    code: ErrorCode = Field(..., description=_ERROR_CODE_DESCRIPTION)

    class Config(TrimModel.Config):
        orm_mode = True


class DetailError(BaseError):
    detail: str = Field(..., description='The error detail')


@with_literal_default
class ModelNotFoundPublicError(BaseError):
    code: Literal[ErrorCode.model_not_found_error] = Field(..., description=_ERROR_CODE_DESCRIPTION)
    columns_names: TupleStr = Field(..., description='The names of columns that was used for search')
    values: TupleStr = Field(..., description='The values that was used for search')


class ModelNotFoundError(ModelNotFoundPublicError):
    table_name: str = Field(..., description='The name of table where row wasn`t found')


@with_literal_default
class UnknownPublicError(BaseError):
    code: Literal[ErrorCode.unknown_error] = Field(..., description=_ERROR_CODE_DESCRIPTION)


class ValidationError(TrimModel):
    loc: List[str | int] = Field(..., title='Location')
    msg: str = Field(..., title='Message')
    type: str = Field(..., title='Error Type')


@with_literal_default
class RequestValidationError(BaseError):
    code: Literal[ErrorCode.request_validation_error] = Field(..., description=_ERROR_CODE_DESCRIPTION)
    detail: List[ValidationError] = Field(..., title='Detail')


class UnknownError(UnknownPublicError, DetailError):
    pass
