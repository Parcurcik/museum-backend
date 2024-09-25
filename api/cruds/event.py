from sqlalchemy import select

from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import EventORM


@with_model(EventORM)
class Event(Base):
    pass
