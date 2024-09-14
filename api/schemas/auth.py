from pydantic import BaseModel
from typing import Optional
from pydantic import EmailStr


class VerificationCodeGet(BaseModel):
    code: str


class PhoneNumberGet(BaseModel):
    number: str


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str


class LoginRequest(BaseModel):
    number: str
    code: str
