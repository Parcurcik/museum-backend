from sqlalchemy import select

from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import VisitorCategoryORM


@with_model(VisitorCategoryORM)
class EventVisitorCategory(Base):
    pass
