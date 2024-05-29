from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Callable

from api.models import UserORM
from api.configuration.database import Session
from api.cruds import User
from api.dependencies import get_session
from api.utils.auth import decode_access_token
from api.models.enums import UserRoleEnum
from api.utils.common import all_in, any_in
from api.exceptions import IncorrectUserRolesError

apiKey_scheme = APIKeyHeader(
    name='authorization', description='The authorization token with service in format service.token', auto_error=False
)


async def get_current_user(
        token: str = Depends(apiKey_scheme),
        session: Session = Depends(get_session)
) -> UserORM:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = await User.get_user_by_email(session, email)
        if user is None:
            raise credentials_exception
        return user

    except Exception:
        raise


def get_user_with_roles(*roles: UserRoleEnum, all_required: bool = False) -> Callable[[UserORM], UserORM]:
    if len(roles) <= 1:
        all_required = True

    async def get_user(current_user: UserORM = Depends(get_current_user)) -> UserORM:

        user_roles = tuple(user_role.role for user_role in current_user.roles)
        if all_required:
            is_right_user = all_in(roles, user_roles)
        else:
            is_right_user = any_in(roles, user_roles)
        if is_right_user:
            return current_user
        raise IncorrectUserRolesError(roles, all_required)

    return get_user


get_admin_user = get_user_with_roles(UserRoleEnum.admin)
