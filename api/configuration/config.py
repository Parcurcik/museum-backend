from dotenv import load_dotenv
import os
from pydantic import BaseSettings, AnyHttpUrl
from typing import List

load_dotenv()


class Settings(BaseSettings):
    # base
    WORKERS: int = 1
    VERSION: str = os.getenv('1.0.0', 'VERSION')
    HOST = 'localhost'
    PREFIX: str = '/api/v1'
    PORT: int = 5000
    RELOAD: bool = False
    CORS_ORIGINS: List[AnyHttpUrl] = []
    CORS_ORIGIN_REGEX: str | None = None
    # database
    DATABASE_URL: str = os.getenv('', 'DATABASE_URL')
    # auth
    JWT_SECRET_KEY: str = os.getenv('', 'JWT_SECRET_KEY')
    JWT_ALGORITHM: str = os.getenv('', 'JWT_ALGORITHM')
    JWT_TOKEN_EXPIRES: int = os.getenv('JWT_TOKEN_EXPIRES', 7)
    # S3
    S3_EVENT_FILES_DIR: str = 'event'
    S3_EXHIBIT_FILES_DIR: str = 'exhibit'
    S3_BUCKET: str = os.getenv('', 'S3_BUCKET')
    S3_ACCESS_KEY: str = os.getenv('', 'S3_ACCESS_KEY')
    S3_SECRET_KEY: str = os.getenv('', 'S3_SECRET_KEY')
    S3_URL: str = os.getenv('', 'S3_URL')
    # email
    EMAIL_HOST: str = os.getenv('', 'EMAIL_HOST')
    EMAIL_USERNAME: str = os.getenv('', 'EMAIL_USERNAME')
    EMAIL_PASSWORD: str = os.getenv('', 'EMAIL_PASSWORD')
    EMAIL_PORT: int = os.getenv('', 'EMAIL_PORT')


class LocalSettings(Settings):
    RELOAD = True


class DevSettings(Settings):
    WORKERS: int = 4
    CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:5173",
        "http://музеум.рф",
        "http://xn--e1adoc6ac.xn--p1ai"
    ]
    CORS_ORIGIN_REGEX = r'(http:\/\/localhost:5173|http:\/\/музеум\.рф|http:\/\/127\.0\.0\.1:5000|http:\/\/xn--e1adoc6ac\.xn--p1ai)'


settings_by_name = {
    'dev': DevSettings,
    'local': LocalSettings,
}

settings = settings_by_name[os.getenv('API_MODE') or 'local']()
