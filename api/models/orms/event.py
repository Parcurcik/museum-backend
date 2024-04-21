from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Table, UniqueConstraint, \
    Integer
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM
from api.models.mixin.date import now, ekt_now


class EventORM(BaseORM, DateORMMixin):
    event_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    disabilities = Column(Boolean)
    started_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False, server_default=ekt_now())

    visitor_age = relationship(
        'EventVisitorAgeORM',
        back_populates='event',
        foreign_keys='[EventVisitorAgeORM.event_id]',
        uselist=True,
        lazy='selectin'
    )

    genre = relationship(
        'EventGenreORM',
        back_populates='event',
        foreign_keys='[EventGenreORM.event_id]',
        uselist=True,
        lazy='selectin'
    )

    event_location = relationship(
        'EventLocationORM',
        back_populates='event',
        foreign_keys='[EventLocationORM.event_id]',
        uselist=True,
        lazy='selectin'
    )

    files = relationship(
        'EventFileORM',
        back_populates='event',
        foreign_keys='[EventFileORM.event_id]',
        uselist=True,
        lazy='selectin'
    )
