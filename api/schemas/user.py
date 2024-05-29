from pydantic import BaseModel
from typing import Optional
from pydantic import EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    name: str
    surname: str
    patronymic: str

    class Config:
        orm_mode = True


class UserCreate(BaseUser):
    password: str


class UserGet(BaseUser):
    user_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Login(BaseModel):
    email: EmailStr
    password: str
