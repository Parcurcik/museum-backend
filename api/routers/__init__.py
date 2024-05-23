from fastapi import Depends, FastAPI
from fastapi.routing import APIRouter

from api.configuration.config import settings as app_settings
from api.dependencies import memorize_request_body
from api.routers import (
    event,
    entity,
    exhibit
)


def init(app: FastAPI) -> None:
    router = APIRouter(prefix=app_settings.PREFIX, dependencies=[Depends(memorize_request_body)])
    modules = [
        event,
        entity,
        exhibit
    ]
    for module in modules:
        router.include_router(module.site_router)
    app.include_router(router)


__all__ = ('init',)
