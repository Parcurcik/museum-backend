from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_session
from api.configuration.database import Session
from api.utils.types import ResponseType
from api import schemas
from api.cruds import User
from api.utils.auth import verify_password, create_access_token

site_router = APIRouter(prefix='/auth', tags=['auth'])


@site_router.post(
    '/register',
    response_model=schemas.UserGet,
    status_code=201,
    responses={
        201: {'description': 'User created'},
        422: {'description': 'Validation error', 'model': schemas.RequestValidationError},
        500: {'description': 'Internal server error', 'model': schemas.BaseInternalError},
    },
)
async def register(
        user: schemas.UserCreate,
        session: Session = Depends(get_session),
) -> ResponseType:
    existing_user = await User.get_user_by_email(session, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = await User.create_user(session, user)
    return new_user.__dict__


@site_router.post(
    '/token',
    response_model=schemas.Token,
    responses={
        200: {'description': 'Success'},
        422: {'description': 'Validation error', 'model': schemas.RequestValidationError},
        500: {'description': 'Internal server error', 'model': schemas.BaseInternalError | schemas.DBInternalError},
    },
)
async def get_token(
        form_data: schemas.Login,
        session: Session = Depends(get_session),
) -> ResponseType:
    user = await User.get_user_by_email(session, form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token}
