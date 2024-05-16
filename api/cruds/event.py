from sqlalchemy import select

from api.cruds.base import Base, with_model
from api.configuration.database import Session
from api.utils.common import now
from api.models import EventORM


@with_model(EventORM)
class Event(Base):

    @classmethod
    async def get_upcoming(cls, session: Session, quantity: int):
        query = select(EventORM).filter(EventORM.started_at > now()).order_by(
            EventORM.started_at.asc()).limit(quantity)
        result = await session.execute(query)
        return result.scalars().all()
