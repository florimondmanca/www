from starlette.applications import Starlette

from . import endpoints, event_handlers, settings
from .middleware import middleware
from .routes import routes

app = Starlette(
    debug=settings.DEBUG,
    routes=routes,
    middleware=middleware,
    exception_handlers={404: endpoints.not_found, 500: endpoints.internal_server_error},
    on_startup=event_handlers.on_startup,
    on_shutdown=event_handlers.on_shutdown,
)
