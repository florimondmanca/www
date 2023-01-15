from typing import Iterator

import pytest

from server.main import get_config

from .util import Server


@pytest.fixture(scope="session")
def server() -> Iterator[Server]:
    config = get_config()
    server = Server(config)
    with server.run_in_thread():
        yield server
