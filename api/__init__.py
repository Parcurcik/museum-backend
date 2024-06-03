from fastapi import FastAPI, Request
from typing import Optional, Awaitable, Callable
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from .exceptions import init as init_exceptions
from api.configuration.config import settings
from api.configuration.database import connect_db, disconnect_db
from api.utils.common import log_request_middleware

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

    @app.middleware('http')
    async def log_request(
            request: Request, call_next: Callable[[Request], Awaitable[StreamingResponse]]
    ) -> StreamingResponse:
        return await log_request_middleware(request, call_next)

    return app


def get_app() -> FastAPI:
    global _app

    if _app is None:
        _app = _init_app()
    return _app
