from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from api import schemas
from api.cruds import User
from api.configuration.database.db_helper import db_helper
from api.utils.auth import generate_verification_code, create_tokens
from api.service.redis import redis_service
from api.bot.whatsapp import whatsapp_bot

site_router = APIRouter(prefix="/auth", tags=["auth"])


@site_router.post(
    "/send_code",
    response_model=schemas.VerificationCodeGet,
    status_code=200,
    responses={
        200: {"description": "Verification code sent"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
)
async def send_code(
        phone: schemas.PhoneNumberGet,
) -> Response:
    verification_code = await generate_verification_code()
    await redis_service.redis.set(phone.number, verification_code, ex=300)

    # # response = whatsapp_bot.send_message(phone.number, f"Ваш код авторизации: {verification_code}")
    #
    # if response.get("status") != "success":
    #     raise HTTPException(status_code=400, detail="Failed to send verification code")

    return {"code": verification_code}


@site_router.post(
    "/login",
    response_model=schemas.TokensResponse,
    status_code=200,
    responses={
        200: {"description": "Verification code validated and token generated"},
        422: {"description": "Validation error"},
        400: {"description": "Invalid verification code"},
        500: {"description": "Internal server error"},
    },
)
async def verify_code(
        login: schemas.LoginRequest,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    # Проверка кода в Redis
    stored_code = await redis_service.redis.get(login.number)
    if stored_code is None or stored_code != login.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    await redis_service.redis.delete(login.number)

    user = await User.get_user_by_phone(session, login.number)
    if not user:
        user = await User.create(session, {"number": login.number})

    access_token, refresh_token = create_tokens(user)

    return {"access_token": access_token, "refresh_token": refresh_token}
