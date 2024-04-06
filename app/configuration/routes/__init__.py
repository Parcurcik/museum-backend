from app.configuration.routes.routes import Routes
from app.internal.routers import user

__routes__ = Routes(routers=(user.router, ))