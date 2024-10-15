from sqlalchemy import select

from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import EventORM


@with_model(EventORM)
class Event(Base):

    @classmethod
    async def update_image_url(cls, session: AsyncSession, event_id: int, image_url: str) -> EventORM:
        event = await cls.get_by_id(session, event_id)
        event.image_url = image_url
        await session.commit()
        await session.refresh(event)
        return event
