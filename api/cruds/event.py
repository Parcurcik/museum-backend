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
            genre_ids: List[int] = None,
            location_ids: List[int] = None,
            visitor_categories: List[int] = None,
            disabilities: bool = None,
            offset: int = 0,
            limit: int = 10,
    ) -> List[schemas.EventBase]:

        query = select(EventORM)

        if genre_ids:
            query = query.filter(EventORM.genre_id.in_(genre_ids))

        if location_ids is not None:
            query = query.filter(EventORM.location_id.in_(location_ids))

        if visitor_categories:
            query = query.join(event_visitor_category_association).filter(
                event_visitor_category_association.c.visitor_category_id.in_(visitor_categories)
            )

        if disabilities is not None:
            query = query.filter(EventORM.disabilities == disabilities)

        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        print(query)
        return result.scalars().all()
