from sqlalchemy import BigInteger, Column, ForeignKey, Index, Integer, Enum
from sqlalchemy.orm import relationship

from api.models.orms.base import BaseORM
from api.models.mixin import DateORMMixin
from api.models.enums import GenreEnum


class EventGenreORM(BaseORM, DateORMMixin):
    event_genre_id = Column(BigInteger, primary_key=True)
    event_id = Column(ForeignKey('event.event_id', ondelete='CASCADE'), nullable=False)
    name = Column(Enum(GenreEnum), nullable=False)

    event = relationship(
        'EventORM',
        back_populates='genre',
        foreign_keys=[event_id],
        uselist=False,
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<{self.__tablename__} {self.event_id} {self.genre}>'
