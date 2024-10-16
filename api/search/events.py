from sqlalchemy import select, func, or_
import math

from sqlalchemy.ext.asyncio import AsyncSession
from api.models import EventORM, EventLocationORM, EventTagORM
from api.schemas import EventSearch


async def _get_info_results(session, query, page, limit):
    total_record_query = select(func.count()).select_from(query)
    total_record = await session.execute(total_record_query)
    total_record = total_record.scalar()

    query = query.offset((page - 1) * limit).limit(limit)
    events = await session.execute(query)
    events = events.scalars().all()

    total_pages = math.ceil(total_record / limit)

    return total_record, events, total_pages


async def search_events(
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
    genre: str = None,
    age: str = None,
    area: str = None,
    disabilities: bool = None,
):
    query = select(EventORM)

    if genre:
        genre_filters = [EventORM.genre.any(name=genre_name) for genre_name in genre]
        query = query.filter(or_(*genre_filters))
    if area:
        area_filters = [
            EventORM.event_location.any(EventLocationORM.area.has(name=area))
            for area in area
        ]
        query = query.filter(or_(*area_filters))

    if disabilities is not None:
        query = query.filter(EventORM.disabilities == disabilities)

    if age:
        area_filters = [EventORM.visitor_age.any(name=age) for age in age]
        query = query.filter(or_(*area_filters))

    total_record, events, total_pages = await _get_info_results(
        session, query, page, limit
    )

    return EventSearch(
        page_number=page,
        page_size=limit,
        pages_total=total_pages,
        total=total_record,
        content=events,
    )


async def find_individual_events(
    session: AsyncSession,
    genre: str = None,
    tags: str = None,
):
    query = select(EventORM)

    if genre:
        genre_filters = [EventORM.genre.any(name=genre_name) for genre_name in genre]
        query = query.filter(or_(*genre_filters))

    if tags:
        tags_filters = [EventTagORM.tags.contains([tag_name]) for tag_name in tags]
        query = query.join(
            EventTagORM, EventORM.event_id == EventTagORM.event_id
        ).filter(or_(*tags_filters))

    events = await session.execute(query)
    return events.scalars().all()
