from typing import Any, Callable, Type, TypeVar

from fastapi import Request

from api import schemas
from api.utils.types import DictStrAny


class ExceptionWithCode(Exception):
    code: str
    admin_schema: Type[schemas.BaseError]
    public_schema: Type[schemas.BaseError] = schemas.BaseError

    def __init__(self, *args: Any) -> None:
        super(ExceptionWithCode, self).__init__(*args)


_ExceptionWithCodeT = TypeVar('_ExceptionWithCodeT', bound=ExceptionWithCode)


def with_schemas(
        admin_schema: Type[schemas.BaseError], public_schema: Type[schemas.BaseError] = schemas.BaseError
) -> Callable[[_ExceptionWithCodeT], _ExceptionWithCodeT]:
    def dec(exc: _ExceptionWithCodeT) -> _ExceptionWithCodeT:
        exc.code = admin_schema.__fields__['code'].default
        exc.admin_schema = admin_schema
        exc.public_schema = public_schema
        return exc

    return dec


@with_schemas(schemas.UnknownError, schemas.UnknownPublicError)
class UnknownError(ExceptionWithCode):
    def __init__(self, orig_exc: Exception) -> None:
        super(UnknownError, self).__init__(orig_exc)
        self.detail = str(orig_exc)


def extract_info(request: Request, exc: ExceptionWithCode) -> DictStrAny:
    state = request.state
    if hasattr(state, 'is_admin_panel') and state.is_admin_panel:
        return exc.admin_schema.from_orm(exc).dict()
    return exc.public_schema.from_orm(exc).dict()
