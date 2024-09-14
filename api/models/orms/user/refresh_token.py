from sqlalchemy import BigInteger, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from api.models.orms.base import BaseORM


class RefreshTokenORM(BaseORM):
    token_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    token = Column(String, nullable=False, unique=True)
    expiration = Column(DateTime, nullable=False)

    user = relationship(
        "UserORM", back_populates="refresh_tokens", foreign_keys=[user_id], lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.user_id} {self.token_id}>"
