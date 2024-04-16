from typing import Callable, TypeVar, Type
from sqlalchemy import select, insert

from api.models import BaseORM
from api.utils.types import PKType, DictStrAny
from api.configuration.database import Session
from api.exceptions import ModelNotFoundError


class Base:
    model = BaseORM

    @classmethod
    def create_object(cls, data: DictStrAny) -> model:
        return cls.model(**data)

    @classmethod
    async def get_by_id(cls, session: Session, id_: PKType) -> model | None:
        query = select(cls.model).where(cls.model.get_pk_column() == id_)
        return await session.fetch_one(query)

    @classmethod
    async def check_existence(cls, session: Session, id_: PKType) -> model:
        object_ = await cls.get_by_id(session, id_)
        if object_ is None:
            raise ModelNotFoundError(cls.model.__tablename__, (cls.model.get_pk_name(),), (str(id_),))
        return object_

    @classmethod
    async def create_and_save(cls, session: Session, data: DictStrAny) -> model:
        object_ = cls.create_object(data)
        stmt = insert(cls.model)
        pk_name = cls.model.get_pk_name()
        pk_value = (await session.execute(stmt, [object_.__dict__])).inserted_primary_key[0]
        try:
            await session.commit()
        except Exception as err:
            raise err
        setattr(object_, pk_name, pk_value)
        return object_


_BaseCRUDT = TypeVar('_BaseCRUDT', bound=Base)


def with_model(model: Type[BaseORM]) -> Callable:
    def dec(crud: _BaseCRUDT) -> _BaseCRUDT:
        crud.model = model
        model.crud = crud
        return crud

    return dec
