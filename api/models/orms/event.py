from sqlalchemy import BigInteger, Boolean, Column, String, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM
from api.models.enums import VisitorCategoryEnum, EventGenreEnum, TagEventEnum

event_visitor_category_association = Table(
    "event_visitor_category_association",
    BaseORM.metadata,
    Column("event_id", ForeignKey("event.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "visitor_category_id",
        ForeignKey("visitor_category.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

event_tag_association = Table(
    "event_tag_association",
    BaseORM.metadata,
    Column("event_id", ForeignKey("event.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("event_tag.id", ondelete="CASCADE"), primary_key=True),
)


class EventORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    image_url = Column(String, nullable=True)
    disabilities = Column(Boolean, default=False)
    location_id = Column(BigInteger, ForeignKey("location.id"), nullable=True)
    genre_id = Column(BigInteger, ForeignKey("event_genre.id"), nullable=True)

    visitor_category = relationship(
        "VisitorCategoryORM",
        secondary=event_visitor_category_association,
        back_populates="events",
        lazy="selectin",
    )

    genre = relationship(
        "EventGenreORM",
        back_populates="events",
        lazy="selectin",
    )

    location = relationship(
        "LocationORM",
        back_populates="events",
        lazy="selectin",
    )

    tag = relationship(
        "EventTagORM",
        secondary=event_tag_association,
        back_populates="events",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class VisitorCategoryORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    name = Column(Enum(VisitorCategoryEnum), nullable=False)

    events = relationship(
        "EventORM",
        secondary=event_visitor_category_association,
        back_populates="visitor_category",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class EventGenreORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    name = Column(Enum(EventGenreEnum), nullable=False)

    events = relationship(
        "EventORM",
        back_populates="genre",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class EventTagORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    name = Column(Enum(TagEventEnum), nullable=False)

    events = relationship(
        "EventORM",
        secondary=event_tag_association,
        back_populates="tag",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"
