import uvicorn

from alembic import command
from alembic.config import Config
from api import get_app
from api.configuration.config import settings

app = get_app()

if __name__ == "__main__":
    alembic_config = Config("alembic.ini")
    command.upgrade(alembic_config, "head")
    uvicorn.run(
        "api_start:app",
        host="0.0.0.0",
        workers=settings.WORKERS,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
