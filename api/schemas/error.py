from typing import List, Literal, Tuple

from pydantic import ConstrainedFloat, Field, NonNegativeFloat, NonNegativeInt, PositiveFloat, PositiveInt

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


@with_literal_default
class IncorrectFileSizePublicError(BaseError):
    code: Literal[ErrorCode.incorrect_file_size_error] = Field(..., description=_ERROR_CODE_DESCRIPTION)
    file_name: str = Field(..., description='The name of file that has incorrect size')
    file_size: NonNegativeFloat = Field(..., description='The actual file size in MB')
    max_size: PositiveFloat = Field(..., description='The maximum file size in MB')


class IncorrectFileSizeError(IncorrectFileSizePublicError):
    pass


@with_literal_default
class IncorrectFileTypePublicError(BaseError):
    code: Literal[ErrorCode.incorrect_file_type_error] = Field(..., description=_ERROR_CODE_DESCRIPTION)
    file_name: str = Field(..., description='The name of file that has incorrect type')
    file_type: str = Field(..., description='The file type')
    correct_types: TupleStr = Field(..., description='The correct types')


class IncorrectFileTypeError(IncorrectFileTypePublicError):
    pass


class ImageAspectRatio(ConstrainedFloat):
    gt = 0
    le = 1


@with_literal_default
class IncorrectImageSizePublicError(BaseError):
    code: Literal[ErrorCode.incorrect_file_size_error] = Field(..., description=_ERROR_CODE_DESCRIPTION)
    image_name: str = Field(..., description='The name of image that has incorrect size')
    min_size: Tuple[PositiveInt | None, PositiveInt | None] = Field(
        ...,
        description='The minimum image size: width, height. The value "null" means that any positive value is allowed',
    )
    max_size: Tuple[PositiveInt | None, PositiveInt | None] = Field(
        ...,
        description='The maximum image size: width, height. The value "null" means that any positive value is allowed',
    )
    aspect_ratio: Tuple[ImageAspectRatio | None, ImageAspectRatio | None] = Field(
        ...,
        description=(
            'The minimum and maximum image aspect ratio (height / width). '
            'The value "null" means that any value from (0; 1] is allowed'
        ),
    )
    image_size: Tuple[NonNegativeInt, NonNegativeInt] = Field(..., description='The actual image size: width, height')


class IncorrectImageSizeError(IncorrectImageSizePublicError):
    pass
