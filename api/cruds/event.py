from sqlalchemy import select, func

from api.cruds.base import Base, with_model
from api.configuration.database import Session
from api.utils.common import now
from api.models import EventORM, TicketORM


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
