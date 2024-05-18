from sqlalchemy import Column, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from api.models.orms.base import BaseORM


class EventTagORM(BaseORM):
    event_tag_id = Column(BigInteger, primary_key=True)
    event_id = Column(ForeignKey('event.event_id', ondelete='CASCADE'), nullable=False)
    tags = Column(ARRAY(String))

    event = relationship(
        'EventORM',
        back_populates='tags',
        foreign_keys=[event_id],
        uselist=False,
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<{self.__tablename__} {self.event_id} {self.tags}>'
