from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from .session import Session


def _build_async_uri(database_uri: str) -> str:
    if '+asyncpg' not in database_uri:
        database_uri = '+asyncpg:'.join(database_uri.split(':', 1))
    return database_uri


_engine: Optional[AsyncEngine] = None
_session_factory: Optional[sessionmaker] = None


def connect_db(database_uri: str) -> None:
    global _engine, _session_factory

    if _engine is None:
        _engine = create_async_engine(_build_async_uri(database_uri))
    if _session_factory is None:
        _session_factory = sessionmaker(_engine, Session, False, False, False)


async def disconnect_db() -> None:
    if _session_factory is not None:
        _session_factory.close_all()
    if _engine is not None:
        await _engine.dispose()


def create_session() -> Session:
    return _session_factory()
