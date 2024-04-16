from dotenv import load_dotenv
import os

from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('', 'DATABASE_URL')
    PREFIX: str = '/api/v1'
    PORT: int = 8080
    RELOAD = True


settings = Settings()
