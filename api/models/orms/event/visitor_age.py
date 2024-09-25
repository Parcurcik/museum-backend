from sqlalchemy import BigInteger, Boolean, Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM
from api.models.enums import VisitorAgeEnum


class EventVisitorAgeORM(BaseORM, DateORMMixin):
    event_visitor_age_id = Column(BigInteger, primary_key=True)
    event_id = Column(ForeignKey("event.event_id", ondelete="CASCADE"), nullable=False)
    name = Column(Enum(VisitorAgeEnum), nullable=False)

    event = relationship(
        "EventORM",
        back_populates="visitor_age",
        foreign_keys=[event_id],
        uselist=False,
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.event_id} {self.visitor_age}>"
