from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from api.cruds.user import User
from api.configuration.database.db_helper import db_helper
from api.models import UserORM
from api.schemas import UserGet
from api.utils.auth import decode_access_token

apiKey_scheme = APIKeyHeader(
    name="authorization",
    description="The authorization token with service in format service.token",
    auto_error=False,
)


async def get_current_user(
    token: str = Depends(apiKey_scheme),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserORM:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        number: str = payload.get("sub")
        if number is None:
            raise credentials_exception
        user = await User.get_user_by_phone(session, number)
        if user is None:
            raise credentials_exception
        return user

    except Exception:
        raise
