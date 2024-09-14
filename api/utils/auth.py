import random
import string
from jose import jwt
from datetime import datetime, timedelta
from typing import Tuple, Dict
from api.configuration.config import settings
from api.models.orms import UserORM

async def generate_verification_code() -> str:
    return ''.join(random.choices(string.digits, k=6))


def generate_jwt_token(data: Dict[str, any], expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_tokens(user: UserORM) -> Dict[str, str]:
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token_expires = timedelta(days=int(settings.REFRESH_TOKEN_EXPIRE_DAYS))

    access_token = generate_jwt_token(
        data={"sub": user.user_id},
        expires_delta=access_token_expires
    )

    refresh_token = generate_jwt_token(
        data={"sub": user.user_id},
        expires_delta=refresh_token_expires
    )

    return access_token, refresh_token
