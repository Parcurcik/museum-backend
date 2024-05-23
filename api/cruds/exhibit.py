from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.cruds.base import Base, with_model
from api.configuration.database import Session
from api.models import ExhibitORM


@with_model(ExhibitORM)
class Exhibit(Base):
    @classmethod
    async def get_all(cls, session: Session) -> list[ExhibitORM]:
        query = (
            select(cls.model)
            .options(selectinload(cls.model.image))
            .order_by(cls.model.floor, cls.model.number)
        )
        result = await session.execute(query)
        return result.scalars().all()
