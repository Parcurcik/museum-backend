from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from api import schemas
from api.dependencies import get_admin_user, get_session
from api.configuration.database import Session
from api.utils.types import ResponseType
from api.utils.html_renderer import generate_mailing
from api.utils.email import send_mail
from api.cruds import Email, Event

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
    dependencies=[Depends(get_admin_user)],
    response_model=None,
    status_code=201,
    responses=swagger_responses,
)
async def send_email(
        session: Session = Depends(get_session),
) -> ResponseType:
    """Send emails across schedule task"""

    emails = await Email.get_all_emails(session)
    events = await Event.get_upcoming_events_by_location(session)

    html_content = generate_mailing({'locations': events})

    try:
        send_mail(emails, html_content)
        print(html_content)
        return JSONResponse(status_code=200, content="Successfully sent mailing")
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
