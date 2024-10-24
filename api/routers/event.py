from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
    Path,
    UploadFile,
    Query,
)
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api import schemas
from api.cruds import Event, EventGenre, EventTag, EventVisitorCategory, Location
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_current_user, is_admin, get_image_with
from api.models import UserORM
from api.models.enums import FilterEventGenreEnum, FilterVisitorCategoryEnum
from api.utils.image import save_event_image

site_router = APIRouter(prefix="/event", tags=["event"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.post(
    "",
    response_model=schemas.EventBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_event(
        payload: schemas.EventCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: UserORM = Depends(is_admin),
) -> Response:
    new_event = await Event.create(session, payload.dict())
    return new_event


@site_router.get(
    "/filter",
    status_code=200,
    response_model=List[schemas.EventBase],
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def filter_event(
        genre_ids: List[int] = Query(None, description="Жанр"),
        location_ids: List[int] = Query(None, description="Локация"),
        visitor_categories: List[int] = Query(
            None, description="Категория посетителей"
        ),
        disabilities: bool = Query(None, description="Инклюзивность"),
        offset: int = Query(0, ge=0, description="Offset"),
        limit: int = Query(10, gt=0, le=100, description="Limit"),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    events = await Event.filter(
        session,
        genre_ids,
        location_ids,
        visitor_categories,
        disabilities,
        offset,
        limit,
    )
    return events


@site_router.put(
    "",
    response_model=schemas.EventBase,
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def update_event_by_id(
        pyload: schemas.EventUpdate,
        event_id: PositiveInt = Path(..., description="The identifier of event"),
        current_user: UserORM = Depends(is_admin),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    updated_event = await Event.update(
        session, event_id, pyload.dict(exclude_unset=True)
    )
    return updated_event


@site_router.post(
    "/{event_id}/upload_logo",
    status_code=200,
    response_model=schemas.EventBase,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def upload_event_logo_by_id(
        event_id: PositiveInt = Path(..., description="The identifier of event"),
        file: UploadFile = Depends(get_image_with),
        current_user: UserORM = Depends(is_admin),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    image_url = save_event_image(file)
    updated_event = await Event.update_image_url(session, event_id, image_url)
    return updated_event


@site_router.get(
    "/{event_id}",
    response_model=schemas.EventBase,
    status_code=200,
    responses=response_codes,
)
async def get_event_by_id(
        session: AsyncSession = Depends(db_helper.session_getter),
        event_id: PositiveInt = Path(..., description="The identifier of event"),
) -> Response:
    event = await Event.get_by_id(session, event_id)
    return event


@site_router.post(
    "/location",
    response_model=schemas.LocationBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_location(
        payload: schemas.LocationCreate,
        current_user: UserORM = Depends(is_admin),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    new_location = await Location.create(session, payload.dict())
    return new_location


@site_router.get(
    "/location/{location_id}",
    response_model=schemas.LocationBase,
    status_code=200,
    responses=response_codes,
)
async def get_location_by_id(
        session: AsyncSession = Depends(db_helper.session_getter),
        location_id: PositiveInt = Path(..., description="The identifier of location"),
) -> Response:
    location = await Location.get_by_id(session, location_id)
    return location


@site_router.put(
    "/location/{location_id}",
    response_model=schemas.LocationBase,
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def update_location_by_id(
        payload: schemas.LocationUpdate,
        session: AsyncSession = Depends(db_helper.session_getter),
        location_id: PositiveInt = Path(..., description="The identifier of location"),
        current_user: UserORM = Depends(is_admin),
) -> Response:
    updated_location = await Location.update(
        session, location_id, payload.dict(exclude_unset=True)
    )
    return updated_location


@site_router.get(
    "/visitor_category/{visitor_category_id}",
    response_model=schemas.EventVisitorCategoryBase,
    status_code=200,
    responses=response_codes,
)
async def get_visitor_category_by_id(
        session: AsyncSession = Depends(db_helper.session_getter),
        visitor_category_id: PositiveInt = Path(
            ..., description="The identifier of visitor category"
        ),
) -> Response:
    visitor_category = await EventVisitorCategory.get_by_id(
        session, visitor_category_id
    )
    return visitor_category


@site_router.get(
    "/genre/{genre_id}",
    response_model=schemas.EventGenreBase,
    status_code=200,
    responses=response_codes,
)
async def get_event_genre_by_id(
        session: AsyncSession = Depends(db_helper.session_getter),
        genre_id: PositiveInt = Path(..., description="The identifier of genre"),
) -> Response:
    genre = await EventGenre.get_by_id(session, genre_id)
    return genre


@site_router.get(
    "/tag/{tag_id}",
    response_model=schemas.EventTagBase,
    status_code=200,
    responses=response_codes,
)
async def get_event_tag_by_id(
        session: AsyncSession = Depends(db_helper.session_getter),
        tag_id: PositiveInt = Path(..., description="The identifier of tag"),
) -> Response:
    tag = await EventTag.get_by_id(session, tag_id)
    return tag
