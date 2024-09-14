from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel


class EventEntities(BaseModel):
    area: Optional[Dict[str, str]]
    genre: Optional[Dict[str, str]]
    visitor_age: Optional[Dict[str, str]]
    tags: Optional[Dict[str, str]]


class EventEntitiesTypes(str, Enum):
    area = "area"
    genre = "genre"
    visitor_age = "visitor_age"
    tags = "tags"
