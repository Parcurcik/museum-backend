from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM


class LocationORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)

    events = relationship(
        "EventORM",
        back_populates="location",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.location_id} {self.name}>"
