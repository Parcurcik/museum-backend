from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.mixin.date import DateORMMixin
from app.models.orms.Base import BaseORM


class Events(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    category = Column(ForeignKey('category.id'))
    price = Column(ForeignKey('cost.id'))
    location = Column(ForeignKey('location.id'))
    name = Column(String)
    description = Column(String)
    disabilities = Column(Boolean)
