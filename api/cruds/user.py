from sqlalchemy import select

from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import UserORM


@with_model(UserORM)
class User(Base):
    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email: str):
        query = select(UserORM).where(UserORM.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_user_by_phone(
        cls, session: AsyncSession, phone_number: str
    ) -> UserORM:
        query = select(UserORM).where(UserORM.number == phone_number)
        result = await session.execute(query)
        return result.scalars().first()
