from sqlalchemy import BigInteger, String, Column, Enum, ForeignKey
from sqlalchemy.orm import relationship

from api.models.orms.base import BaseORM
from api.models.mixin.date import DateORMMixin
from api.models.enums import UserRoleEnum


class UserRoleORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(UserRoleEnum), nullable=False)

    user = relationship(
        "UserORM", back_populates="roles", foreign_keys=[user_id], lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.user_id} {self.role.name}>"
