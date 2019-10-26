import pytest
from starlette.testclient import TestClient
from apps.web import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app, base_url="")
