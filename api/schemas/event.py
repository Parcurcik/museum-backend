from typing import Optional
from datetime import datetime
from pydantic import validator, BaseModel

from enum import Enum


class GenreFilterType(str, Enum):
    excursion = "excursion"
    master_class = "master_class"
    spectacle = "spectacle"
    exhibition = "exhibition"
    interactive_lesson = "interactive_lesson"
    concert = "concert"
    genealogy = "genealogy"
    lecture = "lecture"
    creative_meeting = "creative_meeting"
    festival = "festival"
    artist_talk = "artist_talk"
    film_screening = "film_screening"


class VisitorAgeFilterType(str, Enum):
    adults = "adults"
    teenagers = "teenagers"
    kids = "kids"


class AreaFilterType(str, Enum):
    cachka_house = "cachka_house"
    metenkov_house = "metenkov_house"
    l52 = "l52"
    water_tower = "water_tower"
    makletsky_house = "makletsky_house"
    memorial_complex = "memorial_complex"


class TagEventFilterType(str, Enum):
    architecture = "architecture"
    literature = "literature"
    science = "science"
    history_of_ussr = "history_of_ussr"
    history_of_yekaterinburg = "history_of_yekaterinburg"
    poetry = "poetry"
    music = "music"
    philosophy = "philosophy"
    flora_and_fauna = "flora_and_fauna"
    handmade = "handmade"
    cinematography = "cinematography"
    cartoons = "cartoons"
    tourism = "tourism"
    genealogy = "genealogy"
    paleontology = "paleontology"
    archaeology = "archaeology"


class EventGenreBase(BaseModel):
    name: GenreEnum

    class Config:
        orm_mode = True


class AreaBase(BaseModel):
    name: str
    address: Optional[str]
    phone: Optional[str]

    class Config:
        orm_mode = True


class EventLocationBase(BaseModel):
    event_location_id: int
    area: AreaBase

    class Config:
        orm_mode = True


class EventTagBase(BaseModel):
    tag_id: int
    name: str

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    event_id: int
    name: str
    description: str
    image_url: Optional[str]
    disabilities: bool

    visitor_age: List[EventVisitorAgeBase]
    genre: List[EventGenreBase]
    event_location: List[EventLocationBase]
    tags: List[EventTagBase]

    class Config:
        orm_mode = True
