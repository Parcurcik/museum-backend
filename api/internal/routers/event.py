import asyncio
from typing import Type, List
from pydantic import PositiveInt
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File

from api import schemas
from api.models import EventORM
from api.dependencies import get_session
from api.configuration.database import Session
from api.utils.types import ResponseType


site_router = APIRouter(
    prefix='/exposition',
    tags=['exposition'])

swagger_responses = {
    200: {'description': 'Success'},
    401: {'description': 'Unauthorized'},
    422: {'description': 'Validation error'},
    500: {
        'description': 'Internal server error'
    },
}


@site_router.get(
    '/event/{event_id}',
    response_model=schemas.EventGet,
    responses=swagger_responses,
)
async def get_event_by_id(
    event_id: PositiveInt = Path(..., description='The identifier of event to get'),
    session: Session = Depends(get_session),
) -> ResponseType:
    """Get company by identifier"""
    event = await Event.check_existence(session, event_id)
    return event
