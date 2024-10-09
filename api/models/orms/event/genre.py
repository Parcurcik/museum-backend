from sqlalchemy import BigInteger, Column, ForeignKey, Index, Integer, Enum
from sqlalchemy.orm import relationship

from api.models.orms.base import BaseORM
from api.models.mixin import DateORMMixin
from api.models.enums import EventGenreEnum


class EventGenreORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    event_id = Column(ForeignKey("event.id", ondelete="CASCADE"), nullable=False)
    name = Column(Enum(EventGenreEnum), nullable=False)

    event = relationship(
        "EventORM",
        back_populates="genre",
        foreign_keys=[event_id],
        uselist=False,
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.event_id} {self.name}>"
