import httpx
import pytest

from server import settings

from .utils import find_rel_me_links, find_webmention_url, parse_hcard, parse_hentry


@pytest.mark.asyncio
async def test_webmentions_url(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev"
    response = await client.get(url)
    assert response.status_code == 200
    html = response.text

    webmention_url = find_webmention_url(html)
    assert webmention_url == "https://webmention.io/testserver/webmention"


@pytest.mark.asyncio
async def test_rel_me_links(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev"
    response = await client.get(url)
    assert response.status_code == 200
    html = response.text

    urls = find_rel_me_links(html)
    assert urls == [link["href"] for link in settings.SOCIAL_LINKS]


@pytest.mark.asyncio
async def test_hcard(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev"
    response = await client.get(url)
    assert response.status_code == 200
    html = response.text

    hcard = parse_hcard(html)

    assert hcard == {
        "p-name": "http://florimond.dev/en/",
        "u-url": "http://florimond.dev/en/",
        "u-photo": "http://florimond.dev/static/img/me.png",
    }


@pytest.mark.asyncio
async def test_hentry(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2018/07/let-the-journey-begin"
    response = await client.get(url)
    assert response.status_code == 200
    html = response.text

    hentry = parse_hentry(html)

    assert hentry["p-name"].strip() == "Let the Journey begin"
    assert hentry["p-summary"].strip() == (
        "Hi! My name is Florimond. "
        "I will be your captain for the length of this journey. 👨‍✈️"
    )
    assert hentry["p-author"] == "http://florimond.dev/en/"
    assert hentry["h-card"] == "http://florimond.dev/en/"
    assert hentry["dt-published"] == "2018-07-25"
    assert hentry["e-content"].startswith("Welcome to CodeSail!")
