from sqlalchemy import select
from typing import List

from api.models.enums import FilterVisitorCategoryEnum, FilterEventGenreEnum
from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import EventORM, VisitorCategoryORM, EventGenreORM, LocationORM, event_visitor_category_association
from api import schemas


@with_model(EventORM)
class Event(Base):

    @classmethod
    async def update_image_url(
            cls, session: AsyncSession, event_id: int, image_url: str
    ) -> EventORM:
        event = await cls.get_by_id(session, event_id)
        event.image_url = image_url
        await session.commit()
        await session.refresh(event)
        return event

    @classmethod
    async def filter(
            cls,
            session: AsyncSession,
            genre: List[int] = None,
            location: List[int] = None,
            visitor_category: List[int] = None,
            disabilities: bool = None,
            offset: int = 0,
            limit: int = 10,
    ) -> List[schemas.EventBase]:

        query = select(EventORM)

        if genre:
            query = query.filter(EventORM.genre_id.in_(genre))

        if location is not None:
            query = query.filter(EventORM.location_id.in_(location))

        if visitor_category:
            query = query.join(event_visitor_category_association).filter(
                event_visitor_category_association.c.visitor_category_id.in_(visitor_category)
            )

        if disabilities is not None:
            query = query.filter(EventORM.disabilities == disabilities)

        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        print(query)
        return result.scalars().all()
