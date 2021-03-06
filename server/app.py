from starlette.applications import Starlette

from . import event_handlers, settings, views
from .middleware import middleware
from .routes import routes

app = Starlette(
    debug=settings.DEBUG,
    routes=routes,
    middleware=middleware,
    exception_handlers={404: views.not_found, 500: views.internal_server_error},
    on_startup=event_handlers.on_startup,
    on_shutdown=event_handlers.on_shutdown,
)
