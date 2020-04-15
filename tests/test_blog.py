import typing

import httpx
import pytest

from .utils import find_meta_tags, load_xml_from_string

pytestmark = pytest.mark.asyncio


async def test_root(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


async def test_article(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


async def test_article_no_trailing_slash(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 307
    assert resp.headers["Location"] == (
        "https://florimond.dev/blog/articles/2018/07/let-the-journey-begin/"
    )


async def test_tag(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/blog/tag/python/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]


async def test_not_found(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/blog/foo"
    resp = await client.get(url)
    assert resp.status_code == 404
    assert "text/html" in resp.headers["content-type"]


async def test_internal_server_error(silent_client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/error"
    resp = await silent_client.get(url)
    assert resp.status_code == 500
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.parametrize("resource", ("/sitemap.xml", "/robots.txt"))
async def test_seo_resources(client: httpx.AsyncClient, resource: str) -> None:
    url = f"http://florimond.dev{resource}"
    resp = await client.get(url)
    assert resp.status_code == 200


async def test_rss_feed(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/feed.rss"
    resp = await client.get(url)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/rss+xml"
    load_xml_from_string(resp.text)


async def test_rss_link(client: httpx.AsyncClient) -> None:
    resp = await client.get("http://florimond.dev/")
    line = next(
        (
            l
            for l in resp.text.split("\n")
            if l.strip().startswith('<link rel="alternate" type="application/rss+xml"')
        ),
        None,
    )
    assert line is not None
    assert 'href="https://florimond.dev/feed.rss"' in line


async def test_meta(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]

    meta = find_meta_tags(resp.text)

    def find_meta(typ: str, value: str) -> typing.Optional[dict]:
        for item in meta:
            if item.get(typ) == value:
                return item
        return None

    assert find_meta("name", "description") is not None
    assert find_meta("name", "image") is not None
    assert find_meta("name", "twitter:title") is not None
    assert find_meta("name", "twitter:description") is not None
    assert find_meta("name", "twitter:image") is not None
    assert find_meta("property", "og:title") is not None
    assert find_meta("property", "og:description") is not None
    assert find_meta("property", "og:image") is not None


@pytest.mark.parametrize(
    "resource",
    [
        "/static/fonts/eb-garamond/regular.ttf",
        "/static/fonts/eb-garamond/medium.ttf",
        "/static/fonts/eb-garamond/bold.ttf",
        "/static/fonts/eb-garamond/italic.ttf",
    ],
)
async def test_caching(client: httpx.AsyncClient, resource: str) -> None:
    url = f"http://florimond.dev{resource}"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200, resp.url
    assert "cache-control" in resp.headers
    assert "max-age=3600" in resp.headers["cache-control"]
