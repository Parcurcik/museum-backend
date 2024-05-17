from sqlalchemy import BigInteger, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from api.models.orms.base import BaseORM
from api.models.mixin import DateORMMixin
from api.models.mixin.date import now, ekt_now


class TicketORM(BaseORM, DateORMMixin):
    ticket_id = Column(BigInteger, primary_key=True)
    event_id = Column(ForeignKey('event.event_id', ondelete='CASCADE'), nullable=False)
    date = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False, server_default=ekt_now())

    event = relationship(
        'EventORM',
        back_populates='ticket',
        foreign_keys=[event_id],
        uselist=False,
        lazy='selectin'
    )

    price = relationship(
        'TicketPriceORM',
        back_populates='ticket',
        foreign_keys='[TicketPriceORM.ticket_id]',
        uselist=False,
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<{self.__tablename__} {self.ticket_id} {self.event_id}>'
