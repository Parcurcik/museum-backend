from typing import Any, Tuple

from api.utils.types import TupleStr
from .. import schemas
from .common import ExceptionWithCode, with_schemas


@with_schemas(schemas.IncorrectFileSizeError, schemas.IncorrectFileSizePublicError)
class IncorrectFileSizeError(ExceptionWithCode):
    def __init__(self, file_name: str, file_size: float, max_size: float) -> None:
        super(IncorrectFileSizeError, self).__init__(file_name, file_size, max_size)
        self.file_name = file_name
        self.file_size = file_size
        self.max_size = max_size


@with_schemas(schemas.IncorrectFileTypeError, schemas.IncorrectFileTypePublicError)
class IncorrectFileTypeError(ExceptionWithCode):
    def __init__(self, file_name: str, file_type: str, correct_types: TupleStr) -> None:
        super(IncorrectFileTypeError, self).__init__(file_name, file_type, correct_types)
        self.file_name = file_name
        self.file_type = file_type
        self.correct_types = correct_types


@with_schemas(schemas.IncorrectImageSizeError, schemas.IncorrectImageSizePublicError)
class IncorrectImageSizeError(ExceptionWithCode):
    def __init__(
            self,
            image_name: str,
            image_size: Tuple[int, int],
            min_width: int | None,
            min_height: int | None,
            max_width: int | None,
            max_height: int | None,
            min_aspect_ratio: float | None,
            max_aspect_ratio: float | None,
    ) -> None:
        super(IncorrectImageSizeError, self).__init__(
            image_name, image_size, min_width, min_height, max_width, max_height, min_aspect_ratio, max_aspect_ratio
        )
        self.image_name = image_name
        self.image_size = image_size
        self.min_size = (min_width, min_height)
        self.max_size = (max_width, max_height)
        self.aspect_ratio = (min_aspect_ratio, max_aspect_ratio)
