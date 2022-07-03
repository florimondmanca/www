import typing

import httpx
import pytest

from server.resources import page_repository

from .utils import find_meta_tags, load_xml_from_string


@pytest.mark.asyncio
async def test_root(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/"
    resp = await client.get(url)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_article(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2018/07/let-the-journey-begin/"
    resp = await client.get(url)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_article_no_trailing_slash(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2018/07/let-the-journey-begin"
    resp = await client.get(url)
    assert resp.status_code == 307
    assert resp.headers["Location"] == (
        "http://florimond.dev/en/posts/2018/07/let-the-journey-begin/"
    )


@pytest.mark.asyncio
async def test_tag(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/tag/python/"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]

    url = "http://florimond.dev/fr/tag/test/"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]
    assert "Tutoriels" in resp.text  # Navbar


@pytest.mark.asyncio
async def test_extra_content_dirs(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2020/01/test-draft/"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]

    url = "http://florimond.dev/fr/posts/2021/04/test-brouillon/"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]
    assert "Tutoriels" in resp.text  # Navbar


@pytest.mark.asyncio
async def test_private_link(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2020/01/test-draft-prv-1/"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]
    assert "private link" in resp.text.lower()
    assert "do not share" in resp.text.lower()


KNOWN_CATEGORIES = ["tutorials", "essays", "retrospectives"]


def test_known_categories() -> None:
    pages = page_repository.find_all_category_pages()
    categories = [page.frontmatter.category for page in pages]
    assert categories == KNOWN_CATEGORIES


@pytest.mark.asyncio
@pytest.mark.parametrize("category", KNOWN_CATEGORIES)
async def test_category(client: httpx.AsyncClient, category: str) -> None:
    url = f"http://florimond.dev/en/category/{category}/"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_category_i18n(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/fr/category/tutorials/"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]
    assert "Tutoriels" in resp.text  # Navbar


@pytest.mark.asyncio
async def test_not_found(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/foo"
    resp = await client.get(url, follow_redirects=True)
    assert resp.status_code == 404
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_internal_server_error(silent_client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/error"
    resp = await silent_client.get(url, follow_redirects=True)
    assert resp.status_code == 500
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
@pytest.mark.parametrize("resource", ("/sitemap.xml", "/robots.txt"))
async def test_seo_resources(client: httpx.AsyncClient, resource: str) -> None:
    url = f"http://florimond.dev{resource}"
    resp = await client.get(url)
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_rss_feed(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/feed.rss"
    resp = await client.get(url)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/rss+xml"
    load_xml_from_string(resp.text)


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_meta(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2018/07/let-the-journey-begin/"
    resp = await client.get(url)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]

    meta = find_meta_tags(resp.text)

    def find_meta(typ: str, value: str) -> typing.Optional[dict]:
        for item in meta:
            if item.get(typ) == value:
                return item.get("content")
        return None

    meta_url = "https://florimond.dev/en/posts/2018/07/let-the-journey-begin/"
    assert find_meta("name", "description") is not None
    assert find_meta("name", "image") is not None
    assert find_meta("name", "twitter:url") == meta_url
    assert find_meta("name", "twitter:title") is not None
    assert find_meta("name", "twitter:description") is not None
    assert find_meta("name", "twitter:image") is not None
    assert find_meta("property", "og:url") == meta_url
    assert find_meta("property", "og:title") is not None
    assert find_meta("property", "og:description") is not None
    assert find_meta("property", "og:image") is not None
