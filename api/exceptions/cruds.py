from typing import Any

from api import schemas
from api.utils.types import TupleStr
from .common import ExceptionWithCode, with_schemas


@with_schemas(schemas.ModelNotFoundError, schemas.ModelNotFoundPublicError)
class ModelNotFoundError(ExceptionWithCode):
    def __init__(self, table_name: str, columns_names: TupleStr, values: TupleStr, *args: Any) -> None:
        super(ModelNotFoundError, self).__init__(table_name, columns_names, values, *args)
        self.table_name = table_name
        self.columns_names = columns_names
        self.values = values
