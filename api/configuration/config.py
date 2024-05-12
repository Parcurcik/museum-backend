from dotenv import load_dotenv
import os

from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Base
    WORKERS: int = 1
    PREFIX: str = '/api/v1'
    PORT: int = 8080
    RELOAD = True
    # DataBase
    DATABASE_URL: str = os.getenv('', 'DATABASE_URL')
    # S3
    S3_EVENT_FILES_DIR: str = 'event'
    S3_BUCKET: str = os.getenv('', 'S3_BUCKET')
    S3_ACCESS_KEY: str = os.getenv('', 'S3_ACCESS_KEY')
    S3_SECRET_KEY: str = os.getenv('', 'S3_SECRET_KEY')
    S3_URL: str = os.getenv('', 'S3_URL')


settings = Settings()
