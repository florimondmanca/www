import pytest

from server.utils import is_static_asset


@pytest.mark.parametrize(
    "url, is_static",
    [
        ("/", False),
        ("/blog/", False),
        ("/static-typing/", False),
        ("/feed.rss", True),
        ("/feed.rss/", True),
        ("/static", True),
        ("/static/", True),
        ("/static/fonts/roboto.ttf", True),
    ],
)
def test_is_static_asset(url: str, is_static: bool) -> None:
    assert is_static_asset(url) == is_static
