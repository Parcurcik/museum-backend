from sqlalchemy import BigInteger, Column, ForeignKey, String, Float, Enum
from sqlalchemy.orm import relationship

from api.models.orms.base import BaseORM
from api.models.enums import TicketTypeEnum


class EventPriceORM(BaseORM):
    price_id = Column(BigInteger, primary_key=True)
    event_id = Column(ForeignKey('event.event_id', ondelete='CASCADE'), nullable=False)
    price_type = Column(Enum(TicketTypeEnum), nullable=False)
    price = Column(Float, nullable=False)

    event = relationship(
        'EventORM',
        back_populates='prices',
        foreign_keys=[event_id],
        uselist=False,
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<{self.__tablename__} {self.price_id} {self.event_id}>'
