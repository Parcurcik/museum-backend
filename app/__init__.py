from fastapi import FastAPI

from app.configuration.server import Server


def create_app(_=None) -> FastAPI:
    app = FastAPI(
        title='MUSEUM API',
        description='API for MUSEUM',
        openapi_url=f'/api/v1/openapi.json',
        docs_url=f'/api/v1/docs',
        redoc_url=f'/api/v1//redoc',
        swagger_ui_parameters={'docExpansion': 'none', 'displayRequestDuration': True, 'filter': True},
    )

    return Server(app).get_app()
