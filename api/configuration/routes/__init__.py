from api.configuration.routes.routes import Routes
from api.internal.routers import user, event


__routes__ = Routes(routers=(user.site_router, event.site_router, ))
