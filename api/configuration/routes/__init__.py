from api.configuration.routes.routes import Routes
from api.internal.routers import user

__routes__ = Routes(routers=(user.router, ))