from fastapi import FastAPI
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from .exceptions import init as init_exceptions
from api.configuration.config import settings
from api.configuration.database import connect_db, disconnect_db

_app: Optional[FastAPI] = None


def _init_app() -> FastAPI:
    from .routers import init as init_routers

    app = FastAPI(
        title='MUSEUM API',
        description='API for MUSEUM',
        version=settings.VERSION,
        openapi_url=f'{settings.PREFIX}/openapi.json',
        docs_url=f'{settings.PREFIX}/docs',
        redoc_url=f'{settings.PREFIX}/redoc',
        swagger_ui_parameters={'docExpansion': 'none', 'displayRequestDuration': True, 'filter': True},
    )
    
    if len(settings.CORS_ORIGINS) > 0 or settings.CORS_ORIGIN_REGEX is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            allow_origin_regex=settings.CORS_ORIGIN_REGEX,
        )

    init_exceptions(app)
    init_routers(app)

    @app.on_event('startup')
    async def startup_event() -> None:
        connect_db(settings.DATABASE_URL)

    @app.on_event('shutdown')
    async def shutdown_event() -> None:
        await disconnect_db()

    return app


def get_app() -> FastAPI:
    global _app

    if _app is None:
        _app = _init_app()
    return _app
