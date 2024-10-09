from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from api.configuration.config import settings
from api.utils.base import camel_case_to_snake_case

class BaseORM(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.NAMING_CONVENTION,
    )

    @declared_attr.directive
    def __model_name__(cls) -> str:
        return cls.__name__[:-3]

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__model_name__)}"
