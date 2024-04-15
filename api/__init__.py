from fastapi import FastAPI

from api.configuration.server import Server
from .exceptions import init as init_exceptions
from api.configuration.config import settings


def main_api(_=None) -> FastAPI:
    app = FastAPI(
        title='MUSEUM API',
        description='API for MUSEUM',
        openapi_url=f'{settings.PREFIX}/openapi.json',
        docs_url=f'{settings.PREFIX}/docs',
        redoc_url=f'{settings.PREFIX}/redoc',
        swagger_ui_parameters={'docExpansion': 'none', 'displayRequestDuration': True, 'filter': True},
    )
    init_exceptions(app)

    return Server(app).get_app()
