import asyncio
from asyncio import sleep

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from api.configuration.api_answers import ServerSetup


site_router = APIRouter(
    prefix='/user',
    tags=['user']
)


@site_router.get('/hello')
def get_user():
    return {
        'Museum': 'start'
    }


