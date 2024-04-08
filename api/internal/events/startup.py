from api.configuration.config import settings
from api.configuration.database import connect_db


async def startup_event() -> None:
    connect_db(settings.DATABASE_URL)
