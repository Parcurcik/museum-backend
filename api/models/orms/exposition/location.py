from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM

from api.models.enums import AreaEnum


class LocationORM(BaseORM, DateORMMixin):
    location_id = Column(BigInteger, primary_key=True)
    name = Column(Enum(AreaEnum), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)
    phone = Column(String)

