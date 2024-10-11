from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from api.configuration.database.db_helper import db_helper


def get_session() -> AsyncGenerator[AsyncSession, None]:
    return db_helper.session_getter
