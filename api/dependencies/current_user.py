from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from api.configuration.config import settings
from api.cruds.user import User
from api.configuration.database.db_helper import db_helper
from api.models import UserORM
from api.schemas import UserGet

apiKey_scheme = APIKeyHeader(
    name='authorization', description='The authorization token with service in format service.token', auto_error=False
)


async def get_current_user(token: str = Depends(apiKey_scheme)) -> UserORM:
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
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = UserGet(id=user_id)
    except JWTError as e:
        print(e)
        raise credentials_exception

    async for session in db_helper.session_getter():
        user = await User.get_by_id(session, token_data.user_id)
        if user is None:
            raise credentials_exception
        return user
