from contextlib import asynccontextmanager
from typing import AsyncIterator

from starlette.routing import BaseRoute

from .. import settings
from ..di import resolve
from ..infrastructure.database import InMemoryDatabase
from .reload import HotReload
from .routes import get_routes


class DiyPedals:
    def __init__(self) -> None:
        self._routes = get_routes()

    @asynccontextmanager
    async def lifespan(self) -> AsyncIterator[None]:
        db = resolve(InMemoryDatabase)
        hotreload = resolve(HotReload)

        await db.connect()

        if settings.DEBUG:  # pragma: no cover
            await hotreload.startup()

        yield

        if settings.DEBUG:  # pragma: no cover
            await hotreload.shutdown()

    @property
    def routes(self) -> list[BaseRoute]:
        return self._routes


def create_app() -> DiyPedals:
    return DiyPedals()
