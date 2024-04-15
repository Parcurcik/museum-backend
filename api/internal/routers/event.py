import asyncio
from typing import Type, List
from pydantic import PositiveInt
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File

from api import schemas
from api.cruds import Event
from api.dependencies import get_session
from api.configuration.database import Session
from api.utils.types import ResponseType

site_router = APIRouter(
    prefix='/event',
    tags=['event'])

swagger_responses = {
    200: {'description': 'Success'},
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

# # @site_router.delete(
# #     '/event/{event_id}',
# #     status_code=204,
# #     responses=swagger_responses,
# # )
# # async def delete_event_by_id(
# #         event_id: PositiveInt = Path(..., description='The identifier of event'),
# #         session: Session = Depends(get_session),
# # ) -> ResponseType:
# #     """Delete event by identifier"""
# #     event = await EventORM.check_existance(session, event_id)
# #     try:
# #         await session.delete(event)
# #         await session.commit()
# #     except Exception as err:
# #         raise err
#
#
# @site_router.post(
#     '/event/{event_id}',
#     status_code=201,
#     responses=swagger_responses,
# )
# async def create_event(
#         session: Session = Depends(get_session),
# ) -> ResponseType:
#     pass
#
#
# @site_router.patch(
#     '/application/{application_id}',
#     response_model=schemas.MTKApplicationGet,
#     responses=swagger_responses,
# )
# async def update_application_by_id(
#         event_id: PositiveInt = Path(..., description='The identifier of event to update'),
#         session: Session = Depends(get_session),
# ) -> ResponseType:
#     pass
