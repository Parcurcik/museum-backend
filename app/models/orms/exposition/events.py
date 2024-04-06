from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.mixin.date import DateORMMixin
from app.models.orms.Base import BaseORM


class EventORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    genre_id = Column(ForeignKey('genre.genre_id'))
    ticket_id = Column(ForeignKey('ticket.ticket_id'))
    location_id = Column(ForeignKey('location.location_id'))
    age_id = Column(ForeignKey('age.age_id'))
    name = Column(String)
    description = Column(String)
    disabilities = Column(Boolean)
    started_at = Column(DateTime)

    genre = relationship(
        'GenreORM',
        viewonly=True,
        lazy='selectin'
    )
    ticket = relationship(
        'TicketORM',
        viewonly=True,
        lazy='selectin'
    )
    location = relationship(
        'LocationORM',
        viewonly=True,
        lazy='selectin'
    )
    age = relationship(
        'AgeORM',
        viewonly=True,
        lazy='selectin'
    )

