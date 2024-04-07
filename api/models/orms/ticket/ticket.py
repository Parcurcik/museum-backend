from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Table, UniqueConstraint, Integer
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM


class TicketORM(BaseORM, DateORMMixin):
    ticket_id = Column(BigInteger, primary_key=True)
    price = Column(Float)
    quantity = Column(Integer)
    pushkin_card = Column(Boolean)

