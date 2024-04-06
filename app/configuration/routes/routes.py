from dataclasses import dataclass
from fastapi import FastAPI


@dataclass(frozen=True)
class Routes:

    routers: tuple
    prefix: str = '/api/v1'

    def register_routes(self, app: FastAPI):

        for router in self.routers:
            app.include_router(router, prefix="/api/v1")
