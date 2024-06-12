from sqlalchemy import select, func
from collections import defaultdict
import locale

from api.cruds.base import Base, with_model
from api.configuration.database import Session
from api.utils.common import now
from api.models import EventORM, TicketORM, EventLocationORM, AreaORM


@with_model(EventORM)
class Event(Base):

    @classmethod
    async def get_upcoming(cls, session: Session, quantity: int):
        subquery = (
            select(TicketORM.event_id, func.min(TicketORM.date).label('nearest_date'))
            .filter(TicketORM.date > now())
            .group_by(TicketORM.event_id)
            .order_by(func.min(TicketORM.date).asc())
            .limit(quantity)
            .subquery()
        )

        query = (
            select(EventORM, subquery.c.nearest_date)
            .join(subquery, EventORM.event_id == subquery.c.event_id)
            .order_by(subquery.c.nearest_date.asc())
        )

        result = await session.execute(query)
        events = []
        for event, nearest_date in result:
            event_dict = event.__dict__
            event_dict['nearest_date'] = nearest_date
            events.append(event_dict)
        return events

    @classmethod
    async def get_upcoming_events_by_location(cls, session: Session, quantity: int = 2):

        subquery = (
            select(
                EventORM.event_id,
                EventORM.name,
                EventLocationORM.location_id,
                TicketORM.date,
                func.row_number().over(
                    partition_by=EventLocationORM.location_id,
                    order_by=TicketORM.date
                ).label('rank')
            )
            .join(EventLocationORM, EventORM.event_id == EventLocationORM.event_id)
            .join(TicketORM, EventORM.event_id == TicketORM.event_id)
            .filter(TicketORM.date > now())
            .subquery()
        )

        query = (
            select(
                subquery.c.name,
                subquery.c.date,
                AreaORM.name.label('location_name')
            )
            .join(EventLocationORM, subquery.c.location_id == EventLocationORM.location_id)
            .join(AreaORM, EventLocationORM.location_id == AreaORM.area_id)
            .filter(subquery.c.rank <= quantity)
            .order_by(AreaORM.name, subquery.c.date)
        )

        result = await session.execute(query)
        events = result.fetchall()

        location_groups = defaultdict(list)
        for row in events:
            location_groups[row.location_name].append({
                "event_name": row.name,
                "date": row.date.strftime('%d %B, %H:%M')
            })

        final_list = []
        for location_name, events in location_groups.items():
            unique_events = {tuple(event.items()) for event in events}
            unique_events = [dict(event) for event in unique_events]
            location_dict = {
                "location_name": location_name.value,
                "events": unique_events
            }
            final_list.append(location_dict)

        return final_list
