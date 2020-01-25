import asyncio
import os
import typing

import httpx
import pytest
from asgi_lifespan.manager import LifespanManager
from starlette.types import ASGIApp

from .utils import HTTPClient

os.environ["TESTING"] = "True"
os.environ["DEBUG"] = "False"


@pytest.fixture(scope="session")
def event_loop() -> typing.Iterator[asyncio.AbstractEventLoop]:
    """
    Redefine from pytest-asyncio, as the default fixture is function-scoped.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def app() -> typing.AsyncIterator[ASGIApp]:
    import www

    async with LifespanManager(www.app):
        yield www.app


@pytest.fixture(scope="session")
async def client(app: ASGIApp) -> typing.AsyncIterator[HTTPClient]:
    async with HTTPClient(app=app) as client:
        yield client


@pytest.fixture(scope="session")
async def silent_client(app: ASGIApp) -> typing.AsyncIterator[HTTPClient]:
    dispatch = httpx.ASGIDispatch(app, raise_app_exceptions=False)
    async with HTTPClient(dispatch=dispatch) as client:
        yield client
