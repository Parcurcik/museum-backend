from typing import List
from pydantic import PositiveInt, NonNegativeInt
from fastapi import APIRouter, Depends, Path, UploadFile, Query, HTTPException
import asyncpg

from api import schemas
from api.cruds import Event, EventFile
from api.dependencies import get_session, get_image_with
from api.configuration.database import Session
from api.utils.types import ResponseType
from api.utils.s3 import create_s3_url_by_path
from api.search import search_events, search_individual_events
from api.utils.mime_types import IMAGE_BMP, IMAGE_JPG, IMAGE_PNG

site_router = APIRouter(
    prefix='/event',
    tags=['event'])

swagger_responses = {
    200: {'description': 'Success'},
    201: {'description': 'Created'},
    404: {
        'description': 'Not found',
        'model': schemas.ModelNotFoundPublicError,
    },
    422: {'description': 'Validation error', 'model': schemas.RequestValidationError},
}


@site_router.get(
    '/{event_id}',
    response_model=schemas.EventGet,
    responses=swagger_responses,
)
async def get_event_by_id(
        event_id: PositiveInt = Path(..., description='The identifier of event to get'),
        session: Session = Depends(get_session),
) -> ResponseType:
    """Get event by identifier"""
    event = await Event.check_existence(session, event_id)
    return event


@site_router.get(
    '/upcoming/',
    response_model=List[schemas.ShallowEventGet],
    responses=swagger_responses,
)
async def get_upcoming_events(
        quantity: PositiveInt = Query(..., description='The quantity of upcoming events'),
        session: Session = Depends(get_session),

) -> ResponseType:
    """Get upcoming events by quantity"""
    events = await Event.get_upcoming(session, quantity)
    return events


@site_router.get(
    '/search/',
    response_model=schemas.EventSearch,
    responses=swagger_responses
)
async def get_events(
        page: NonNegativeInt = Query(1, description='The search events page number'),
        limit: NonNegativeInt = Query(10, description='The search events limit count'),
        genre: List[schemas.GenreFilterType] = Query(None, description='The genre filter'),
        area: List[schemas.AreaFilterType] = Query(None, description='The area filter'),
        age: List[schemas.VisitorAgeFilterType] = Query(None, description='The age filter'),
        disabilities: bool = Query(None, description='Can event take for people with disabilities'),
        session: Session = Depends(get_session),
) -> ResponseType:
    """Search events by filters"""
    return await search_events(session, page, limit, genre, age, area, disabilities)


@site_router.get(
    '/search_individual/',
    response_model=schemas.EventSearch,
    responses=swagger_responses
)
async def get_individual_events(
        page: NonNegativeInt = Query(1, description='The search events page number'),
        limit: NonNegativeInt = Query(10, description='The search events limit count'),
        genre: List[schemas.GenreFilterType] = Query(None, description='The genre filter'),
        tags: List[schemas.TagEventFilterType] = Query(None, description='User Tags filter'),
        session: Session = Depends(get_session),
) -> ResponseType:
    """Search events by individual filters"""
    return await search_individual_events(session, page, limit, genre, tags)


@site_router.delete(
    '/{event_id}',
    status_code=204,
    responses=swagger_responses,
    
)
async def delete_event_by_id(
        event_id: PositiveInt = Path(..., description='The identifier of event'),
        session: Session = Depends(get_session),
) -> None:
    """Delete event by identifier"""
    event = await Event.check_existence(session, event_id)
    try:
        await session.delete(event)
        await session.commit()
    except Exception as err:
        raise err


@site_router.post(
    '',
    response_model=schemas.EventGet,
    status_code=201,
    responses=swagger_responses,
)
async def create_event(
        payload: schemas.EventCreate,
        session: Session = Depends(get_session),
) -> ResponseType:
    """Create new event"""
    data = payload.dict(exclude_unset=True)
    try:

        application = await Event.create_and_save(session, data)

        return application.__dict__
    except Exception as err:
        raise err


@site_router.patch(
    '/{event_id}',
    response_model=schemas.EventGet,
    responses=swagger_responses,
)
async def update_event_by_id(
        payload: schemas.EventUpdate,
        event_id: PositiveInt = Path(..., description='The identifier of event to update'),
        session: Session = Depends(get_session),
) -> ResponseType:
    """Update event by identifier"""
    event = await Event.check_existence(session, event_id)
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        if isinstance(data[key], list):
            field: list | None = getattr(event, key, None)
            if field is not None:
                field.clear()
        else:
            setattr(event, key, value)
    await session.merge(event)
    try:
        await session.commit()
    except Exception as err:
        raise err
    return event.__dict__


@site_router.post(
    '/{event_id}/logo/upload',
    response_model=schemas.EventLogoCreate,
    responses={
        200: {'description': 'Success'},
        404: {
            'description': 'Not found',
            'model': schemas.ModelNotFoundPublicError,
        },
        400: {
            'description': 'Bad request',
            'model': schemas.IncorrectFileTypePublicError
                     | schemas.IncorrectFileSizePublicError
                     | schemas.IncorrectImageSizePublicError,
        },
    },
)
async def upload_event_logo(
        event_id: PositiveInt = Path(..., description='The identifier of event'),
        event_logo_image: UploadFile = Depends(
            get_image_with(
                'event_card_logo',
                ...,
                content_types=(IMAGE_BMP, IMAGE_JPG, IMAGE_PNG),
                description='Event card image',
            )
        ),
        session: Session = Depends(get_session),
) -> ResponseType:
    """Upload event card image"""
    logo_s3_path = await EventFile.upload_file_on_s3(event_logo_image, True)
    logo_url = create_s3_url_by_path(logo_s3_path)

    data = {
        'name': event_logo_image.filename,
        'description': f'Event {event_id} image',
        's3_path': logo_url,
    }

    try:
        existing_logo = await EventFile.get_by_event_id(session, event_id)
        if existing_logo:
            event_logo = await EventFile.update(session, data, existing_logo.event_logo_id)
            await session.commit()
        else:
            data['event_id'] = event_id
            event_logo = await EventFile.create_and_save(session, data)

    except Exception:
        await EventFile.delete_file_from_s3(logo_url)
        await session.rollback()
        raise

    return event_logo
