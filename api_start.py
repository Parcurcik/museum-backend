import uvicorn

from alembic import command
from alembic.config import Config
from api import main_api
from api.configuration.config import settings

main_api = main_api()

if __name__ == '__main__':
    alembic_config = Config('alembic.ini')
    command.upgrade(alembic_config, 'head')
    uvicorn.run(
        'api:main_api',
        host='0.0.0.0',
        port=settings.PORT,
        reload=settings.RELOAD,
    )
