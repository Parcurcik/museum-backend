import asyncio
from asyncio import sleep

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.configuration.api_answers import ServerSetup


router = APIRouter(
    prefix='/user'
)


@router.get('/hello')
def get_user():
    return {
        'Museum': 'start'
    }


