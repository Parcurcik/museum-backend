from fastapi import Query
from fastapi.routing import APIRouter
from typing import List, Dict, Any

from api import schemas
from api.utils.types import ResponseType
from api.models.enums import GenreEnum, VisitorAgeEnum, AreaEnum

site_router = APIRouter(prefix='/entity', tags=['entity'])


async def _set_entity_result_from_enums(
        result: schemas.EventEntities,
        entity_type: schemas.EventEntitiesTypes,
        entity_mapping: Dict[schemas.EventEntitiesTypes, Any]
) -> None:
    result_dict = {item.name: item.value for item in entity_mapping[entity_type]}
    setattr(result, entity_type, result_dict)


@site_router.get(
    '/event',
    response_model=schemas.EventEntities,
    response_model_exclude_unset=True,
    responses={
        200: {'description': 'Success'},
        422: {'description': 'Validation error', 'model': schemas.RequestValidationError},
        500: {
            'description': 'Internal server error',
            'model': schemas.PublicBaseInternalError | schemas.PublicDBInternalError,
        },
    },
)
async def get_event_entities(
        entities: List[schemas.EventEntitiesTypes] = Query(
            ..., description='Event entities to get'
        ),
) -> ResponseType:
    """Get entities for event"""
    result = schemas.EventEntities()
    entity_mapping = {
        schemas.EventEntitiesTypes.area: AreaEnum,
        schemas.EventEntitiesTypes.genre: GenreEnum,
        schemas.EventEntitiesTypes.visitor_age: VisitorAgeEnum
    }
    for entity in set(entities):
        await _set_entity_result_from_enums(result, entity, entity_mapping)
    return result
