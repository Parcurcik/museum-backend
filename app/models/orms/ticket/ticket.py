from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Table, UniqueConstraint, Integer
from sqlalchemy.orm import relationship

from app.models.mixin.date import DateORMMixin
from app.models.orms.base import BaseORM


class TicketORM(BaseORM, DateORMMixin):
    ticket_id = Column(BigInteger, primary_key=True)
    price = Column(Float)
    quantity = Column(Integer)
    pushkin_card = Column(Boolean)
