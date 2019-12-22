import typing

import httpx
import pytest
from asgi_lifespan.manager import LifespanManager

import web


@pytest.fixture
async def client() -> typing.AsyncIterator[httpx.AsyncClient]:
    async with LifespanManager(web.app):
        async with httpx.AsyncClient(app=web.app) as client:
            yield client
