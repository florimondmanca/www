import asyncio
import typing

import httpx
import pytest
from asgi_lifespan.manager import LifespanManager

import web


@pytest.fixture(scope="session")
def event_loop() -> typing.Iterator[asyncio.AbstractEventLoop]:
    """
    Redefine from pytest-asyncio, as the default fixture is function-scoped.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client() -> typing.AsyncIterator[httpx.AsyncClient]:
    async with LifespanManager(web.app):
        async with httpx.AsyncClient(app=web.app) as client:
            yield client
