from typing import Any, Tuple

from api.utils.types import TupleStr
from api.models.enums import UserRoleEnum
from api import schemas
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


@with_schemas(schemas.PermissionDeniedError, schemas.PermissionDeniedPublicError)
class PermissionDeniedError(ExceptionWithCode):
    def __init__(self, detail: str, *args: Any) -> None:
        super(PermissionDeniedError, self).__init__(detail, *args)
        self.detail = detail


@with_schemas(schemas.IncorrectUserRolesError, schemas.IncorrectUserRolesError)
class IncorrectUserRolesError(PermissionDeniedError):
    def __init__(self, roles: Tuple[UserRoleEnum, ...], all_required: bool = False) -> None:
        super(IncorrectUserRolesError, self).__init__('Incorrect user roles', roles, all_required)
        self.roles = roles
        self.all_required = all_required
