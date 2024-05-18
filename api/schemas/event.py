from typing import Optional
from datetime import datetime
from pydantic import validator

from api.schemas.base import BaseModel, TrimModel
from api.utils.common import format_datetime, format_datetime_with_timezone

from enum import Enum


class GenreFilterType(str, Enum):
    excursion = 'excursion'
    master_class = 'master_class'
    spectacle = 'spectacle'
    exhibition = 'exhibition'
    interactive_lesson = 'interactive_lesson'
    concert = 'concert'
    genealogy = 'genealogy'
    lecture = 'lecture'
    creative_meeting = 'creative_meeting'
    festival = 'festival'
    artist_talk = 'artist_talk'
    film_screening = 'film_screening'


class VisitorAgeFilterType(str, Enum):
    adults = 'adults'
    teenagers = 'teenagers'
    kids = 'kids'


class AreaFilterType(str, Enum):
    cachka_house = 'cachka_house'
    metenkov_house = 'metenkov_house'
    l52 = 'l52'
    water_tower = 'water_tower'
    makletsky_house = 'makletsky_house'
    memorial_complex = 'memorial_complex'


class TagEventFilterType(str, Enum):
    architecture = 'architecture'
    literature = 'literature'
    science = 'science'
    history_of_ussr = 'history_of_ussr'
    history_of_yekaterinburg = 'history_of_yekaterinburg'
    poetry = 'poetry'
    music = 'music'
    philosophy = 'philosophy'
    flora_and_fauna = 'flora_and_fauna'
    handmade = 'handmade'
    cinematography = 'cinematography'
    cartoons = 'cartoons'
    tourism = 'tourism'
    genealogy = 'genealogy'
    paleontology = 'paleontology'
    archaeology = 'archaeology'


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


class EventPriceGet(BaseModel):
    price_type: str
    price: float

    class Config:
        orm_mode = True


class TicketDateGet(BaseModel):
    date: datetime

    @validator('date', pre=True)
    def format_datetime_with_timezone(cls, v):
        return format_datetime_with_timezone(v)

    class Config:
        orm_mode = True


class EventGet(BaseModel):
    event_id: int
    name: str
    description: str
    disabilities: Optional[bool]
    visitor_age: Optional[list[EventVisitorAgeGet]]
    genre: Optional[list[EventGenreGet]]
    event_location: Optional[list[EventLocationGet]]
    ticket_date: Optional[list[TicketDateGet]]
    ticket_price: Optional[list[EventPriceGet]]
    file: Optional[list[EventLogoGet]]

    # _format_datetime = validator('started_at', allow_reuse=True)(format_datetime)

    class Config:
        orm_mode = True


class ShallowEventGet(BaseModel):
    event_id: int
    name: str
    disabilities: Optional[bool]
    nearest_date: datetime
    event_location: Optional[list[EventLocationGet]]
    file: Optional[list[EventLogoGet]]

    @validator('nearest_date', pre=True)
    def format_datetime_with_timezone(cls, v):
        return format_datetime_with_timezone(v)

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


class EventSearch(TrimModel):
    page_number: int
    page_size: int
    pages_total: int
    total: int
    content: list[EventGet]
