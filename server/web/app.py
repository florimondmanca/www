from starlette.applications import Starlette
from starlette.types import ASGIApp

from .. import settings
from . import event_handlers, views
from .middleware import middleware
from .routes import routes


def create_app() -> ASGIApp:
    return Starlette(
        debug=settings.DEBUG,
        routes=routes,
        middleware=middleware,
        exception_handlers={404: views.not_found, 500: views.internal_server_error},
        on_startup=event_handlers.on_startup,
        on_shutdown=event_handlers.on_shutdown,
    )
