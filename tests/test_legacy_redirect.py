import typing

import pytest
from starlette.testclient import TestClient


@pytest.mark.parametrize(
    "start_url, urls",
    [
        pytest.param(
            "http://florimondmanca.com", ["http://florimond.dev/"], id="home",
        ),
        pytest.param(
            "http://blog.florimondmanca.com",
            ["http://blog.florimond.dev/", "http://florimond.dev/blog/"],
            id="blog:home",
        ),
        pytest.param(
            "http://blog.florimondmanca.com/let-the-journey-begin",
            [
                "http://blog.florimond.dev/let-the-journey-begin",
                "http://florimond.dev/blog/let-the-journey-begin",
                "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin",
            ],
            id="blog:article",
        ),
    ],
)
def test_legacy_redirect_chains(
    client: TestClient, start_url: str, urls: typing.List[str]
) -> None:
    resp = client.get(start_url, allow_redirects=True)
    assert resp.status_code == 200
    assert [r.headers["Location"] for r in resp.history] == urls
