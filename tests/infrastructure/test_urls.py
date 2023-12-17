import pytest

from server.infrastructure.urls import get_absolute_path


def test_get_absolute_path_undefined() -> None:
    with pytest.raises(ValueError):
        get_absolute_path(object())
