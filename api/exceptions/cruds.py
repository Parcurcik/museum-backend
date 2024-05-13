from typing import Any, List

from api import schemas
from api.utils.types import TupleStr, PKType
from .common import ExceptionWithCode, with_schemas
from .routers import PermissionDeniedError


class ModelIncorrectDataError(ExceptionWithCode):
    pass


@with_schemas(schemas.ModelNotFoundError, schemas.ModelNotFoundPublicError)
class ModelNotFoundError(ExceptionWithCode):
    def __init__(self, table_name: str, columns_names: TupleStr, values: TupleStr, *args: Any) -> None:
        super(ModelNotFoundError, self).__init__(table_name, columns_names, values, *args)
        self.table_name = table_name
        self.columns_names = columns_names
        self.values = values


@with_schemas(schemas.IncorrectRelationObjectError, schemas.IncorrectRelationObjectPublicError)
class IncorrectRelationObjectError(ModelIncorrectDataError):
    def __init__(
            self, table_name: str, relation_key: str, valid_object_cls: List[type], object_cls: type | str
    ) -> None:
        super(IncorrectRelationObjectError, self).__init__(table_name, relation_key, valid_object_cls, object_cls)
        self.table_name = table_name
        self.relation_key = relation_key
        self.valid_object_cls = [valid_cls.__name__ for valid_cls in valid_object_cls]
        self.object_cls = object_cls.__name__ if not isinstance(object_cls, str) else object_cls


class ModelIncorrectDataError(ExceptionWithCode):
    pass


class DeletionError(PermissionDeniedError):
    def __init__(self, table_name: str, id_: PKType) -> None:
        detail = f'{table_name} ({id_}) can`t be deleted'
        super(DeletionError, self).__init__(detail, table_name, id_)
