import pytest
from starlette.testclient import TestClient

import www


@pytest.fixture
def client() -> TestClient:
    return TestClient(www.app, base_url="")
