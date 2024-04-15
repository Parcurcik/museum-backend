from api.configuration.database import disconnect_db


async def shutdown() -> None:
    await disconnect_db()
