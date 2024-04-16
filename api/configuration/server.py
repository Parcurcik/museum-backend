from fastapi import FastAPI
from api.configuration.routes import __routes__
from api.internal.events import startup_event
from api.internal.events import shutdown


class Server:
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_routes(app)
        self.__register_events(app)

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def __register_events(app):
        app.on_event('startup')(startup_event)
        app.on_event('shutdown')(shutdown)

    @staticmethod
    def __register_routes(app):
        __routes__.register_routes(app)
