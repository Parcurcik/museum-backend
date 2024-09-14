from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from api.configuration.database.db_helper import db_helper


async def disconnect_db() -> None:
    await db_helper.dispose()


async def create_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.session_getter():
        yield session
