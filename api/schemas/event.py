from typing import Optional
from datetime import datetime
from pydantic import validator

from api.schemas.base import BaseModel, TrimModel
from api.utils.common import format_datetime


class EventVisitorAgeCreate(BaseModel):
    event_id: int
    age_name: str


class EventGenreCreate(BaseModel):
    event_id: int
    genre: str


class AreaCreate(BaseModel):
    name: str
    address: str
    phone: str


class EventLocationCreate(BaseModel):
    area: Optional[AreaCreate]


class EventVisitorAgeGet(BaseModel):
    name: str

    class Config:
        orm_mode = True


class EventGenreGet(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AreaGet(BaseModel):
    name: str
    address: str
    phone: str

    class Config:
        orm_mode = True


class EventLocationGet(BaseModel):
    area: Optional[AreaGet]

    class Config:
        orm_mode = True


class EventLogoGet(BaseModel):
    description: str
    s3_path: str

    class Config:
        orm_mode = True


class EventGet(BaseModel):
    event_id: int
    name: str
    description: str
    disabilities: Optional[bool]
    started_at: datetime
    visitor_age: Optional[list[EventVisitorAgeGet]]
    genre: Optional[list[EventGenreGet]]
    event_location: Optional[list[EventLocationGet]]
    files: Optional[list[EventLogoGet]]

    _format_datetime = validator('started_at', allow_reuse=True)(format_datetime)

    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    name: str
    description: str
    disabilities: Optional[bool]
    started_at: datetime


class EventUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    disabilities: Optional[bool]
    started_at: Optional[datetime]


class EventLogoCreate(BaseModel):
    event_logo_id: int
    name: str
    description: str
    s3_path: str

    class Config(TrimModel.Config):
        orm_mode = True
