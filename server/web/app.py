from contextlib import asynccontextmanager
from typing import AsyncIterator

from starlette.applications import Starlette
from starlette.types import ASGIApp

from .. import settings
from ..di import resolve
from ..diypedals.web.app import create_app as create_diypedals
from ..infrastructure.database import InMemoryDatabase
from . import views
from .middleware import middleware
from .reload import HotReload
from .routes import get_routes


def create_app() -> ASGIApp:
    db = resolve(InMemoryDatabase)
    hotreload = resolve(HotReload)

    diypedals = create_diypedals()

    routes = get_routes(diypedals.routes)

    @asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        await db.connect()

        if settings.DEBUG:  # pragma: no cover
            await hotreload.startup()

        async with diypedals.lifespan():
            yield

        if settings.DEBUG:  # pragma: no cover
            await hotreload.shutdown()

    return Starlette(
        debug=settings.DEBUG,
        routes=routes,
        middleware=middleware,
        exception_handlers={404: views.not_found, 500: views.internal_server_error},
        lifespan=lifespan,
    )
