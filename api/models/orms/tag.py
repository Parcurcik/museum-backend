from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM


class TagORM(BaseORM):
    tag_id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    events = relationship("EventTagORM", back_populates="tag", lazy="selectin")

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.tag_id} {self.name}>"
