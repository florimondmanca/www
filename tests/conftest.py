import asyncio
import os
from typing import AsyncIterator, Iterator

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from starlette.types import ASGIApp

os.environ["TESTING"] = "True"
os.environ["DEBUG"] = "False"
os.environ["EXTRA_CONTENT_DIRS"] = "tests/drafts"


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    """
    Redefine from pytest-asyncio, as the default fixture is function-scoped.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncIterator[ASGIApp]:
    from server.main import app

    async with LifespanManager(app):
        yield app


@pytest_asyncio.fixture(scope="session")
async def client(app: ASGIApp) -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def silent_client(app: ASGIApp) -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app, raise_app_exceptions=False)
    async with httpx.AsyncClient(transport=transport) as client:
        yield client


@pytest.fixture
@pytest.mark.usefixtures("app")
def isolated_db() -> Iterator[None]:
    from server.di import resolve
    from server.infrastructure.database import InMemoryDatabase

    db = resolve(InMemoryDatabase)

    with db.isolated():
        yield
