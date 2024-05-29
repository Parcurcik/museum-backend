from typing import List
from pydantic import PositiveInt, NonNegativeInt
from fastapi import APIRouter, Depends, Path, UploadFile, Query, HTTPException
import asyncpg

from api import schemas
from api.cruds import ExhibitFile, Exhibit
from api.dependencies import get_session, get_image_with, get_admin_user
from api.configuration.database import Session
from api.utils.types import ResponseType
from api.utils.s3 import create_s3_url_by_path
from api.utils.mime_types import IMAGE_BMP, IMAGE_JPG, IMAGE_PNG

site_router = APIRouter(
    prefix='/exhibit',
    tags=['exhibit'])

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
    '/{exhibit_id}/logo/upload',
    dependencies=[Depends(get_admin_user)],
    response_model=schemas.ExhibitLogoCreate,
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
async def upload_exhibit_image(
        exhibit_id: PositiveInt = Path(..., description='The identifier of exhibit'),
        exhibit_image: UploadFile = Depends(
            get_image_with(
                'exhibit_image',
                ...,
                content_types=(IMAGE_BMP, IMAGE_JPG, IMAGE_PNG),
                description='Exhibit image',
            )
        ),
        session: Session = Depends(get_session),
) -> ResponseType:
    """Upload exhibit image"""
    logo_s3_path = await ExhibitFile.upload_file_on_s3(exhibit_image, True)
    logo_url = create_s3_url_by_path(logo_s3_path)
    data = {
        'name': exhibit_image.filename,
        'description': f'Exhibit {exhibit_id} image',
        's3_path': logo_url,
    }

    try:
        existing_image = await ExhibitFile.get_by_exhibit_id(session, exhibit_id)
        if existing_image:
            exhibit_image = await ExhibitFile.update(session, data, existing_image.exhibit_logo_id)
            await session.commit()
        else:
            data['exhibit_id'] = exhibit_id
            exhibit_image = await ExhibitFile.create_and_save(session, data)

    except Exception:
        await ExhibitFile.delete_file_from_s3(logo_url)
        await session.rollback()
        raise

    return exhibit_image


@site_router.get(
    '/{exhibit_id}',
    response_model=schemas.ExhibitGet,
    responses=swagger_responses,
)
async def get_exhibit_by_id(
        exhibit_id: PositiveInt = Path(..., description='The identifier of exhibit to get'),
        session: Session = Depends(get_session),
) -> ResponseType:
    """Get exhibit by identifier"""
    exhibit = await Exhibit.check_existence(session, exhibit_id)
    return exhibit


@site_router.post(
    '',
    dependencies=[Depends(get_admin_user)],
    response_model=schemas.ExhibitGet,
    status_code=201,
    responses=swagger_responses,
)
async def create_exhibit(
        payload: schemas.ExhibitCreate,
        session: Session = Depends(get_session),
) -> ResponseType:
    """Create new exhibit"""
    data = payload.dict(exclude_unset=True)
    try:

        exhibit = await Exhibit.create_and_save(session, data)

        return exhibit.__dict__
    except Exception as err:
        raise err


@site_router.delete(
    '/{exhibit_id}',
    dependencies=[Depends(get_admin_user)],
    status_code=204,
    responses=swagger_responses,
)
async def delete_exhibit_by_id(
        exhibit_id: PositiveInt = Path(..., description='The identifier of exhibit to delete'),
        session: Session = Depends(get_session),
) -> None:
    """Delete exhibit by identifier"""
    exhibit = await Exhibit.check_existence(session, exhibit_id)
    try:
        await session.delete(exhibit)
        await session.commit()
    except Exception as err:
        raise err


@site_router.patch(
    '/{exhibit_id}',
    dependencies=[Depends(get_admin_user)],
    response_model=schemas.ExhibitGet,
    responses=swagger_responses,
)
async def update_exhibit_by_id(
        payload: schemas.ExhibitUpdate,
        exhibit_id: PositiveInt = Path(..., description='The identifier of exhibit to update'),
        session: Session = Depends(get_session),
) -> ResponseType:
    """Update exhibit by identifier"""
    exhibit = await Exhibit.check_existence(session, exhibit_id)
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        if isinstance(data[key], list):
            field: list | None = getattr(exhibit, key, None)
            if field is not None:
                field.clear()
        else:
            setattr(exhibit, key, value)
    await session.merge(exhibit)
    try:
        await session.commit()
    except Exception as err:
        raise err
    return exhibit.__dict__


@site_router.get(
    '/all/',
    response_model=List[schemas.ExhibitGet],
    responses=swagger_responses,
)
async def get_exhibits(
        session: Session = Depends(get_session),

) -> ResponseType:
    """Get all exhibits"""
    exhibits = await Exhibit.get_all(session)
    return exhibits
