from typing import Callable, TypeVar, Type, Any, Dict, List, Tuple, Set
from sqlalchemy import select, insert, inspect
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import BaseORM


class Base:
    model: Type[BaseORM]

    @classmethod
    async def create(cls, session: AsyncSession, data: Dict[str, Any]) -> BaseORM:
        obj = cls.model(**data)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> BaseORM:
        primary_key_column = inspect(cls.model).primary_key[0]
        query = select(cls.model).where(primary_key_column == id_)
        result = await session.execute(query)
        obj = result.scalar_one_or_none()
        if obj is None:
            raise ModelNotFoundError(cls.model.__tablename__, "id", id_)
        return obj

    @classmethod
    async def update(
        cls, session: AsyncSession, id_: int, data: Dict[str, Any]
    ) -> BaseORM:
        obj = await cls.get_by_id(session, id_)
        for key, value in data.items():
            setattr(obj, key, value)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def delete(cls, session: AsyncSession, id_: int) -> None:
        obj = await cls.get_by_id(session, id_)
        await session.delete(obj)
        await session.commit()


_BaseCRUDT = TypeVar("_BaseCRUDT", bound=Base)


def with_model(model: Type[BaseORM]) -> Callable[[_BaseCRUDT], _BaseCRUDT]:
    def wrapper(crud_class: _BaseCRUDT) -> _BaseCRUDT:
        crud_class.model = model
        return crud_class

    return wrapper
