from dotenv import load_dotenv
import os
from pydantic import BaseSettings, AnyHttpUrl
from typing import List

load_dotenv()


class Settings(BaseSettings):
    # base
    WORKERS: int = 1
    VERSION: str = os.getenv("1.0.0", "VERSION")
    HOST = "localhost"
    PREFIX: str = "/api"
    PORT: int = 8000
    RELOAD: bool = False
    CORS_ORIGINS: List[AnyHttpUrl] = []
    CORS_ORIGIN_REGEX: str | None = None
    # database
    DATABASE_URL: str = os.getenv("", "DATABASE_URL")
    ECHO: bool = False
    ECHO_POOL: bool = False
    POOL_SIZE: int = 50
    MAX_OVERFLOW: int = 10
    NAMING_CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    # auth
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_TOKEN_EXPIRES: int = int(os.getenv("JWT_TOKEN_EXPIRES", 7))
    ACCESS_TOKEN_EXPIRE_MINUTES: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: str = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
    # redis
    REDIS_HOST = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    # S3
    S3_EVENT_FILES_DIR: str = "event"
    S3_EXHIBIT_FILES_DIR: str = "exhibit"
    S3_BUCKET: str = os.getenv("", "S3_BUCKET")
    S3_ACCESS_KEY: str = os.getenv("", "S3_ACCESS_KEY")
    S3_SECRET_KEY: str = os.getenv("", "S3_SECRET_KEY")
    S3_URL: str = os.getenv("", "S3_URL")
    # email
    SMTP_HOST: str = os.getenv("", "EMAIL_HOST")
    SMTP_USERNAME: str = os.getenv("", "EMAIL_USERNAME")
    SMTP_PASSWORD: str = os.getenv("", "EMAIL_PASSWORD")
    SMTP_PORT: str = os.getenv("", "EMAIL_PORT")
    SMTP_SENDER: str = os.getenv("", "SMTP_SENDER")
    # whatsapp
    API_URL: str = os.getenv("", "API_URL")
    INSTANCE_ID: str = os.getenv("", "INSTANCE_ID")
    API_TOKEN: str = os.getenv("", "API_TOKEN")
    AUTH_MESSAGE_TEMPLATE: str = os.getenv("", "AUTH_MESSAGE_TEMPLATE")


class LocalSettings(Settings):
    RELOAD = True


class DevSettings(Settings):
    WORKERS: int = 4
    CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:5173",
        "http://музеум.рф",
        "http://xn--e1adoc6ac.xn--p1ai",
    ]
    CORS_ORIGIN_REGEX = r"(http:\/\/localhost:5173|http:\/\/музеум\.рф|http:\/\/127\.0\.0\.1:5000|http:\/\/xn--e1adoc6ac\.xn--p1ai)"


settings_by_name = {
    "dev": DevSettings,
    "local": LocalSettings,
}

settings = settings_by_name[os.getenv("API_MODE") or "local"]()
