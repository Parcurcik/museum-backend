from sqlalchemy import select

from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import EventGenreORM


@with_model(EventGenreORM)
class EventGenre(Base):
    pass
