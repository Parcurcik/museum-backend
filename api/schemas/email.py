from api.schemas.base import BaseModel

from pydantic import EmailStr


class EmailGet(BaseModel):
    email_id: int
    email: str

    class Config:
        orm_mode = True


class EmailCreate(BaseModel):
    email: EmailStr
