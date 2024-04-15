from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM

from api.models.enums import AreaEnum


class AreaORM(BaseORM, DateORMMixin):
    area_id = Column(BigInteger, primary_key=True)
    name = Column(Enum(AreaEnum), nullable=False)
    address = Column(String)
    phone = Column(String)

    area = relationship(
        'EventLocationORM',
        back_populates='area',
        foreign_keys='[EventLocationORM.location_id]',
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<{self.__tablename__} {self.location_id} {self.name}>'
