from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM


class EventORM(BaseORM, DateORMMixin):
    event_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    image_url = Column(String, nullable=True)
    disabilities = Column(Boolean, default=False)

    visitor_age = relationship(
        "EventVisitorAgeORM",
        back_populates="event",
        foreign_keys="[EventVisitorAgeORM.event_id]",
        uselist=True,
        lazy="selectin",
    )

    genre = relationship(
        "EventGenreORM",
        back_populates="event",
        foreign_keys="[EventGenreORM.event_id]",
        uselist=True,
        lazy="selectin",
    )

    event_location = relationship(
        "EventLocationORM",
        back_populates="event",
        foreign_keys="[EventLocationORM.event_id]",
        uselist=True,
        lazy="selectin",
    )

    tags = relationship(
        "EventTagORM",
        back_populates="event",
        foreign_keys="[EventTagORM.event_id]",
        uselist=False,
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.event_id} {self.name}>"
