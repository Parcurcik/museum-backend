from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.mixin.date import DateORMMixin
from app.models.orms.Base import BaseORM

from app.models.enums import AgeEnum


class AgeORM(BaseORM, DateORMMixin):
    age_id = Column(BigInteger, primary_key=True)
    name = Column(Enum(AgeEnum), nullable=False)


