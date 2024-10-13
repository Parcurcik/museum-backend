from pydantic import BaseModel


class ErrorNotFound(BaseModel):
    message: str


class ErrorGeneral(BaseModel):
    message: str
    detail: str
