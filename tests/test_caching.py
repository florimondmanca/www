import httpx
import pytest


@pytest.mark.parametrize(
    "resource",
    [
        "/static/fonts/eb-garamond/regular.ttf",
        "/static/fonts/eb-garamond/medium.ttf",
        "/static/fonts/eb-garamond/bold.ttf",
        "/static/fonts/eb-garamond/italic.ttf",
    ],
)
@pytest.mark.asyncio
async def test_caching(client: httpx.AsyncClient, resource: str) -> None:
    url = f"http://florimond.dev{resource}"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200, resp.url
    assert "cache-control" in resp.headers
    assert "max-age=3600" in resp.headers["cache-control"]
