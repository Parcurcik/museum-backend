from typing import Tuple

from asyncpg.exceptions import (
    CheckViolationError,
    ForeignKeyViolationError,
    IntegrityConstraintViolationError,
    NotNullViolationError,
    PostgresError,
    UniqueViolationError,
)
from sqlalchemy.exc import DBAPIError as DBAPIError_
from sqlalchemy.exc import IntegrityError as IntegrityError_
from sqlalchemy.exc import OperationalError as OperationalError_

from .. import schemas
from ..utils.types import TupleStr
from .common import ExceptionWithCode, with_schemas

SQLADBAPIError = DBAPIError_
SQLAOperationalError = OperationalError_
SQLAIntegrityError = IntegrityError_

PSQLError = PostgresError

PSQLIntegrityError = IntegrityConstraintViolationError
PSQLCheckViolationError = CheckViolationError
PSQLForeignKeyViolationError = ForeignKeyViolationError
PSQLNotNullViolationError = NotNullViolationError
PSQLUniqueViolationError = UniqueViolationError


def get_info_from_check_violation_error(error: PSQLCheckViolationError) -> str:
    return error.constraint_name


def get_info_from_foreign_key_violation_error(error: PSQLForeignKeyViolationError) -> Tuple[TupleStr, TupleStr, str]:
    detail_msg = ' is not present in table'
    right_index = error.detail.rfind(detail_msg)
    fields, values = error.detail[4:right_index].split('=', 1)
    fields = tuple(s.strip() for s in fields[1:-1].split(','))
    values = tuple(s.strip() for s in values[1:-1].split(','))
    foreign_table_name = error.detail[right_index + len(detail_msg):].strip()[1:-2]
    return fields, values, foreign_table_name


def get_info_from_not_null_violation_error(error: PSQLNotNullViolationError) -> str:
    return error.column_name


def get_info_from_unique_violation_error(error: PSQLUniqueViolationError) -> Tuple[TupleStr, TupleStr]:
    fields, values = error.detail[4:-16].split('=', 1)
    fields = tuple(s.strip() for s in fields[1:-1].split(','))
    values = tuple(s.strip() for s in values[1:-1].split(','))
    return fields, values


class _DBError(ExceptionWithCode):
    def __init__(self, orig_exc: SQLADBAPIError) -> None:
        super(_DBError, self).__init__(orig_exc)
        self.detail = str(orig_exc)


@with_schemas(schemas.UnknownDBError, schemas.UnknownDBPublicError)
class UnknownDBError(_DBError):
    pass


@with_schemas(schemas.OperationalError, schemas.OperationalPublicError)
class OperationalError(_DBError):
    pass


@with_schemas(schemas.IntegrityError, schemas.IntegrityPublicError)
class IntegrityError(_DBError):
    pass
