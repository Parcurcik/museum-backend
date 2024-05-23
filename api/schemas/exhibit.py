from typing import Optional
from datetime import datetime
from pydantic import validator

from api.schemas.base import BaseModel, TrimModel


class ExhibitLogoCreate(BaseModel):
    exhibit_logo_id: int
    name: str
    description: str
    s3_path: str

    class Config(TrimModel.Config):
        orm_mode = True


class ExhibitCreate(BaseModel):
    name: str
    description: str
    floor: int
    number: float


class ExhibitUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    floor: Optional[int]
    number: Optional[float]


class ExhibitImageGet(BaseModel):
    s3_path: str

    class Config:
        orm_mode = True


class ExhibitGet(BaseModel):
    exhibit_id: int
    floor: int
    number: float
    name: str
    description: str
    image: Optional[list[ExhibitImageGet]]

    class Config(TrimModel.Config):
        orm_mode = True
