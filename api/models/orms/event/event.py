from sqlalchemy import BigInteger, Boolean, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM


class EventORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    image_url = Column(String, nullable=True)
    disabilities = Column(Boolean, default=False)
    location_id = Column(BigInteger, ForeignKey("location.id"), nullable=True)

    visitor_category = relationship(
        "EventVisitorCategoryORM",
        back_populates="event",
        foreign_keys="[EventVisitorCategoryORM.event_id]",
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

    location = relationship(
        "LocationORM",
        back_populates="events",
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
