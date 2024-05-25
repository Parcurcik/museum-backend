from sqlalchemy import BigInteger, String, Column

from api.models.orms.base import BaseORM
from api.models.mixin.date import DateORMMixin


class EmailORM(BaseORM, DateORMMixin):
    email_id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'<{self.__tablename__} {self.email_id} {self.email}>'
