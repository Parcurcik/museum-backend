from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any

from api.dependencies import get_session
from api.configuration.database import Session
from api.utils.types import ResponseType
from api import schemas
from api.cruds import Email

site_router = APIRouter(prefix='/email', tags=['email'])

swagger_responses = {
    200: {'description': 'Success'},
    201: {'description': 'Created'},
    404: {
        'description': 'Not found',
        'model': schemas.ModelNotFoundPublicError,
    },
    422: {'description': 'Validation error', 'model': schemas.RequestValidationError},
}


@site_router.post(
    '',
    response_model=schemas.EmailGet,
    status_code=201,
    responses=swagger_responses,
)
async def add_email(
        payload: schemas.EmailCreate,
        session: Session = Depends(get_session),
) -> ResponseType:
    """Add email for mailing"""
    data = payload.dict(exclude_unset=True)

    existing_email = await Email.get_by_email(session, data['email'])
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    try:
        email = await Email.create_and_save(session, data)

        return email.__dict__
    except Exception as err:
        raise err


@site_router.post(
    '/send',
    response_model=None,
    status_code=201,
    responses=swagger_responses,
)
async def send_email(
        session: Session = Depends(get_session),
) -> ResponseType:
    """Send email across schedule task"""

    emails = await Email.get_all_emails(session)

    # try:
    #     html_content = generate_application(application_data_dict)
    # except Exception as err:
    #     raise err
