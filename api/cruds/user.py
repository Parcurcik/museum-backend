from sqlalchemy import select

from api.cruds.base import Base, with_model
from api.configuration.database import Session
from api.models import UserORM
from api.schemas import UserCreate
from api.utils.auth import get_password_hash


@with_model(UserORM)
class User(Base):
    @classmethod
    async def get_user_by_email(cls, session: Session, email: str):
        query = select(UserORM).where(UserORM.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def create_user(cls, session: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = UserORM(
            email=user.email,
            name=user.name,
            surname=user.surname,
            patronymic=user.patronymic,
            hashed_password=hashed_password
        )
        try:
            session.add(db_user)
            await session.commit()
        except Exception:
            await session.rollback()
            raise

        return db_user
