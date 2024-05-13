from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .cruds import ModelNotFoundError, DeletionError, ModelIncorrectDataError, IncorrectRelationObjectError
from .common import ExceptionWithCode, UnknownError, extract_info
from .routers import IncorrectFileSizeError, IncorrectFileTypeError, IncorrectImageSizeError
from .db import (CheckViolationError,
                 ForeignKeyViolationError,
                 NotNullViolationError,
                 PSQLCheckViolationError,
                 PSQLForeignKeyViolationError,
                 PSQLIntegrityError,
                 PSQLNotNullViolationError,
                 PSQLUniqueViolationError,
                 UniqueViolationError,
                 get_info_from_check_violation_error,
                 get_info_from_foreign_key_violation_error,
                 get_info_from_not_null_violation_error,
                 get_info_from_unique_violation_error,
                 )


def init(app: FastAPI) -> None:
    @app.exception_handler(ExceptionWithCode)
    def handle_code_error(request: Request, exc: ExceptionWithCode) -> JSONResponse:
        match exc:
            case (
            ModelNotFoundError()
            ):
                status_code = status.HTTP_404_NOT_FOUND
            case (
            ModelIncorrectDataError()
            | IncorrectFileSizeError()
            | IncorrectFileTypeError()
            | IncorrectImageSizeError()
            ):
                status_code = status.HTTP_400_BAD_REQUEST
        content = extract_info(request, exc)
        return JSONResponse(status_code=status_code, content=content)

    @app.exception_handler(Exception)
    def handle_default_error(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=extract_info(request, UnknownError(exc)),
        )


__all__ = (
    'ModelNotFoundError',
    'init',
    'IncorrectFileSizeError',
    'IncorrectFileTypeError',
    'IncorrectImageSizeError',
    'DeletionError',
    'CheckViolationError',
    'ForeignKeyViolationError',
    'NotNullViolationError',
    'PSQLCheckViolationError',
    'PSQLForeignKeyViolationError',
    'PSQLIntegrityError',
    'PSQLNotNullViolationError',
    'PSQLUniqueViolationError',
    'UniqueViolationError',
    'get_info_from_check_violation_error',
    'get_info_from_foreign_key_violation_error',
    'get_info_from_not_null_violation_error',
    'get_info_from_unique_violation_error',
    'IncorrectRelationObjectError',
)
