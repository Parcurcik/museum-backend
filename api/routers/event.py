from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from api import schemas
from api.cruds import User
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_current_user
from api.models import UserORM

site_router = APIRouter(prefix="/event", tags=["event"])


@site_router.get(
    "/{id}",
    response_model=schemas.EventBase,
    status_code=200,
    responses={
        200: {"description": "Event information retrieved successfully"},
        404: {"description": "Not found"},
    },
)
async def get_event_by_id(
        session: AsyncSession = Depends(db_helper.session_getter),
        event_id: PositiveInt = Path(..., description='The identifier of event to get'),
) -> Response:
    event = Event.get_by_id(session, event_id)
    return event


@site_router.put(
    "",
    response_model=schemas.BaseUser,
    status_code=200,
    responses={
        200: {"description": "User information updated successfully"},
        401: {"description": "Unauthorized"},
        404: {"description": "User not found"},
    },
)
async def update_current_user(
        pyload: schemas.UserUpdate,
        current_user: UserORM = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    user_data = pyload.dict(exclude_unset=True)
    updated_user = await User.update(session, current_user.user_id, user_data)

    return updated_user


@site_router.post(
    "",
    response_model=schemas.BaseUser,
    status_code=200,
    responses={
        200: {"description": "User information updated successfully"},
        401: {"description": "Unauthorized"},
        404: {"description": "User not found"},
    },
)
async def update_current_user(
        pyload: schemas.UserUpdate,
        current_user: UserORM = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    user_data = pyload.dict(exclude_unset=True)
    updated_user = await User.update(session, current_user.user_id, user_data)

    return updated_user