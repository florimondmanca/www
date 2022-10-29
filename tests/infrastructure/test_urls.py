import pytest

from server.infrastructure.urls import get_absolute_url


def test_get_absolute_url_undefined() -> None:
    with pytest.raises(ValueError):
        get_absolute_url(object())
