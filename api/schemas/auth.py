from pydantic import BaseModel
from typing import Optional
from pydantic import EmailStr, validator
import re


class VerificationCodeGet(BaseModel):
    code: str


class PhoneNumberGet(BaseModel):
    number: str

    @validator("number")
    def validate_phone_number(cls, value):
        pattern = re.compile(r"^\d{11}$")
        if not pattern.match(value):
            raise ValueError("Invalid phone number format")
        return value


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str


class RefreshTokenGet(BaseModel):
    refresh_token: str


class LoginRequestGet(BaseModel):
    number: str
    code: str
