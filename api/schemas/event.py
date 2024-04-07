from typing import List, Optional
from datetime import date, datetime

from enum import Enum
from pydantic import BaseModel


class TicketGet(BaseModel):
    id: int
    price: float
    quantity: int
    pushkin_card: bool


class AgeGet(BaseModel):
    id: int


class GenreGet(BaseModel):
    id: int


class LocationGet(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    address: str
    phone: str


class EventGet(BaseModel):
    id: int
    name: str
    description: str
    disabilities: bool
    started_at: datetime
    genre: List[GenreGet]
    ticket: List[TicketGet]
    location: List[LocationGet]
    age: List[AgeGet]
