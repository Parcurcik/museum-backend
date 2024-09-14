from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from api import schemas
from api.cruds import User
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_current_user
from api.models import UserORM

site_router = APIRouter(prefix="/user", tags=["user"])


@site_router.get(
    "/me",
    response_model=schemas.UserGet,
    status_code=200,
    responses={
        200: {"description": "User information retrieved successfully"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"},
    },
)
async def get_current_user_data(
        current_user: UserORM = Depends(get_current_user),
) -> Response:
    return current_user
