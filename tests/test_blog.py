import httpx
import pytest

pytestmark = pytest.mark.asyncio


async def test_root(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/blog/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]


async def test_article(client: httpx.AsyncClient) -> None:
    urls = [
        "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin",
        "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin/",
        "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin/index.html",
    ]
    responses = [await client.get(url, allow_redirects=False) for url in urls]
    for resp in responses:
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]
    unique_contents = {resp.text for resp in responses}
    assert len(unique_contents) == 1


async def test_tag(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/blog/tag/python"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]


async def test_not_found(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/blog/foo"
    resp = await client.get(url)
    assert resp.status_code == 404
    assert "text/html" in resp.headers["content-type"]
