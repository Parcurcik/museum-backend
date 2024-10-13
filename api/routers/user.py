from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from api import schemas
from api.cruds import User
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_current_user
from api.models import UserORM

site_router = APIRouter(prefix="/user", tags=["user"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.get(
    "/me",
    response_model=schemas.BaseUser,
    status_code=200,
    responses={
        200: {"description": "Success"},
    },
)
async def get_current_user(
    current_user: UserORM = Depends(get_current_user),
) -> Response:
    return current_user


@site_router.put(
    "",
    response_model=schemas.BaseUser,
    status_code=200,
    responses=response_codes,
)
async def update_current_user(
    pyload: schemas.UserUpdate,
    current_user: UserORM = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    user_data = pyload.dict(exclude_unset=True)
    updated_user = await User.update(session, current_user.id, user_data)

    return updated_user
