from dotenv import load_dotenv
import os

from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # base
    WORKERS: int = 1
    HOST = 'localhost'
    PREFIX: str = '/api/v1'
    PORT: int = 5000
    RELOAD: bool = False
    # database
    DATABASE_URL: str = os.getenv('', 'DATABASE_URL')
    # S3
    S3_EVENT_FILES_DIR: str = 'event'
    S3_BUCKET: str = os.getenv('', 'S3_BUCKET')
    S3_ACCESS_KEY: str = os.getenv('', 'S3_ACCESS_KEY')
    S3_SECRET_KEY: str = os.getenv('', 'S3_SECRET_KEY')
    S3_URL: str = os.getenv('', 'S3_URL')


class LocalSettings(Settings):
    RELOAD = True


class DevSettings(Settings):
    WORKERS: int = 4

    HOST = ''


settings_by_name = {
    'dev': DevSettings,
    'local': LocalSettings,
}

settings = settings_by_name[os.getenv('API_MODE') or 'local']()
