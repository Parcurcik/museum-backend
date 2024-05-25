from sqlalchemy import select

from api.cruds.base import Base, with_model
from api.configuration.database import Session
from api.models import EmailORM


@with_model(EmailORM)
class Email(Base):
    @classmethod
    async def get_by_email(cls, session: Session, email: str):
        query = select(EmailORM).where(EmailORM.email == email)
        result = await session.execute(query)
        return result.scalars().first()
