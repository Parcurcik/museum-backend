from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .cruds import ModelNotFoundError
from .common import ExceptionWithCode, UnknownError, extract_info


def init(app: FastAPI) -> None:
    @app.exception_handler(ExceptionWithCode)
    def handle_code_error(request: Request, exc: ExceptionWithCode) -> JSONResponse:
        match exc:
            case (
            ModelNotFoundError()
            ):
                status_code = status.HTTP_404_NOT_FOUND
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
    'init'
)
