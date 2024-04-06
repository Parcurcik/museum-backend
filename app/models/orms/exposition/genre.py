from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.mixin.date import DateORMMixin
from app.models.orms.base import BaseORM

from app.models.enums import CategoryEnum


class GenreORM(BaseORM, DateORMMixin):
    genre_id = Column(BigInteger, primary_key=True)
    name = Column(Enum(CategoryEnum), nullable=False)


