import typing

import httpx
import pytest

from server.resources import index
from server import settings

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
        "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin/"
    )


async def test_tag(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/blog/tag/python/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]


async def test_images(client: httpx.AsyncClient) -> None:
    # TODO: test URLs to images in Markdown content too.
    for page in index.pages:
        if page.frontmatter.image is None:
            continue

        if page.frontmatter.image.startswith("http"):
            # Remote images should exist.
            url = page.frontmatter.image
            async with httpx.AsyncClient() as http:
                response = await http.get(url)
                assert response.status_code == 200, url
                # TODO: test image sizes.
        else:
            # Local images should exist, and be of reasonable sizes.
            url = f"http://testserver{page.frontmatter.image}"
            response = await client.get(url)
            assert response.status_code == 200, url
            assert (
                len(response.content) / 1024 < settings.IMAGE_ALLOWED_MAX_SIZE_KB
            ), url


KNOWN_CATEGORIES = ["tutorials", "essays", "retrospectives"]


def test_known_categories() -> None:
    pages = index.get_category_pages()
    categories = [page.frontmatter.category for page in pages]
    assert categories == KNOWN_CATEGORIES


@pytest.mark.parametrize("category", KNOWN_CATEGORIES)
async def test_category(client: httpx.AsyncClient, category: str) -> None:
    url = f"http://florimond.dev/blog/category/{category}/"
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
            line
            for line in resp.text.split("\n")
            if line.strip().startswith(
                '<link rel="alternate" type="application/rss+xml"'
            )
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
