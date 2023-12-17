import httpx
import pytest

from server import settings

from .utils import find_rel_me_links, find_webmention_url


@pytest.mark.asyncio
async def test_webmentions_url(client: httpx.AsyncClient) -> None:
    url = "https://florimond.dev"
    response = await client.get(url)
    assert response.status_code == 200
    html = response.text

    webmention_url = find_webmention_url(html)
    assert webmention_url == "https://webmention.io/testserver/webmention"


@pytest.mark.asyncio
async def test_rel_me_links(client: httpx.AsyncClient) -> None:
    url = "https://florimond.dev"
    response = await client.get(url)
    assert response.status_code == 200
    html = response.text

    urls = find_rel_me_links(html)
    assert urls == [link["href"] for link in settings.SOCIAL_LINKS]
