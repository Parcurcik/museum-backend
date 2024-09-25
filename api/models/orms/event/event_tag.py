from sqlalchemy import BigInteger, Boolean, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM


class EventTagORM(BaseORM):
    event_tag_id = Column(BigInteger, primary_key=True)
    event_id = Column(ForeignKey("event.event_id", ondelete="CASCADE"), nullable=False)
    tag_id = Column(ForeignKey("tag.tag_id", ondelete="CASCADE"), nullable=False)

    event = relationship(
        "EventORM",
        back_populates="tags",
        foreign_keys=[event_id],
        uselist=False,
        lazy="selectin",
    )

    tag = relationship("TagORM", back_populates="events", lazy="selectin")

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.event_id} {self.tags}>"
