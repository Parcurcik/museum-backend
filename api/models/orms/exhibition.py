from sqlalchemy import BigInteger, Integer, Column, String, Float
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM


class ExhibitORM(BaseORM, DateORMMixin):
    exhibit_id = Column(BigInteger, primary_key=True)
    floor = Column(Integer)
    number = Column(Float)
    name = Column(String)
    description = Column(String)

    image = relationship(
        'ExhibitFileORM',
        back_populates='exhibit',
        foreign_keys='[ExhibitFileORM.exhibit_id]',
        uselist=True,
        lazy='selectin'
    )
