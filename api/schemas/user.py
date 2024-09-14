from pydantic import BaseModel
from typing import Optional
from pydantic import EmailStr


class UserGet(BaseModel):
    user_id: int


class BaseUser(UserGet):
    email: Optional[EmailStr]
    number: str
    name: Optional[str]
    surname: Optional[str]
