import pytest
from starlette.testclient import TestClient

import web


@pytest.fixture
def client() -> TestClient:
    return TestClient(web.app, base_url="")
