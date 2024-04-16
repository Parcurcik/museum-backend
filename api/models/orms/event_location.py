from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM


class EventLocationORM(BaseORM, DateORMMixin):
    event_location_id = Column(BigInteger, primary_key=True)
    event_id = Column(ForeignKey('event.event_id', ondelete='CASCADE'), nullable=False)
    location_id = Column(ForeignKey('area.area_id', ondelete='CASCADE'), nullable=False)

    event = relationship(
        'EventORM',
        back_populates='event_location',
        foreign_keys=[event_id],
        uselist=False,
        lazy='selectin'
    )

    area = relationship(
        'AreaORM',
        back_populates='area',
        foreign_keys=[location_id],
        uselist=False,
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<{self.__tablename__} {self.event_id} {self.location_id}>'
