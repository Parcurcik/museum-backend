from typing import AsyncIterator

from api.configuration.database import Session, create_session


async def get_session() -> AsyncIterator[Session]:
    session = create_session()
    try:
        yield session
    finally:
        await session.close()
