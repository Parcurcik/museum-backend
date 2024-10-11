from sqlalchemy import BigInteger, String, Column, Enum, ForeignKey
from sqlalchemy.orm import relationship

from api.models.orms.base import BaseORM
from api.models.mixin.date import DateORMMixin


class UserORM(BaseORM, DateORMMixin):
    user_id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=True, unique=True)
    number = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)

    roles = relationship(
        "UserRoleORM",
        back_populates="user",
        foreign_keys="[UserRoleORM.user_id]",
        lazy="selectin",
    )

    refresh_tokens = relationship(
        "RefreshTokenORM",
        back_populates="user",
        foreign_keys="[RefreshTokenORM.user_id]",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.user_id} {self.number}>"
