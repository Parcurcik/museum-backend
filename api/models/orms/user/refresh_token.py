from sqlalchemy import BigInteger, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from api.models.orms.base import BaseORM


class RefreshTokenORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    token = Column(String, nullable=False, unique=True)
    expires = Column(DateTime(timezone=True), nullable=False)

    user = relationship(
        "UserORM",
        back_populates="refresh_tokens",
        foreign_keys=[user_id],
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.user_id} {self.token_id}>"
