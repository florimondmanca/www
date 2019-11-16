import typing

import httpx
import pytest

import www


@pytest.fixture
async def client() -> typing.AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=www.app) as client:
        yield client
