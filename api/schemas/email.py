from pydantic import EmailStr, BaseModel


class EmailGet(BaseModel):
    email_id: int
    email: str

    class Config:
        orm_mode = True


class EmailCreate(BaseModel):
    email: EmailStr
