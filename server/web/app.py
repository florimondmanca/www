from starlette.applications import Starlette
from starlette.types import ASGIApp

from .. import settings
from ..di import resolve
from ..infrastructure.database import InMemoryDatabase
from . import views
from .middleware import middleware
from .reload import HotReload
from .routes import get_routes


def create_app() -> ASGIApp:
    db = resolve(InMemoryDatabase)
    hotreload = resolve(HotReload)

    routes = get_routes()

    on_startup = [db.connect]
    on_shutdown = []

    if settings.DEBUG:  # pragma: no cover
        on_startup += [hotreload.startup]
        on_shutdown += [hotreload.shutdown]

    return Starlette(
        debug=settings.DEBUG,
        routes=routes,
        middleware=middleware,
        exception_handlers={404: views.not_found, 500: views.internal_server_error},
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )
