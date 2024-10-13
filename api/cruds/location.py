from sqlalchemy import select

from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import LocationORM


@with_model(LocationORM)
class Location(Base):
    pass
