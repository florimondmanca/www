import httpx
import pytest

from server.di import resolve
from server.domain.repositories import CategoryRepository

from .utils import find_meta_tags, get_start_tag, load_xml_from_string


@pytest.mark.asyncio
async def test_root(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev"
    resp = await client.get(url)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_root_pagination(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/?page=2"
    resp = await client.get(url)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert '<option value="2" selected>' in resp.text


@pytest.mark.asyncio
async def test_root_hx(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev"
    resp = await client.get(url, headers={"HX-Request": "true"})
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    _, attrs = get_start_tag(resp.text)
    assert attrs["data-testid"] == "post-list"


@pytest.mark.asyncio
async def test_article(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2018/07/let-the-journey-begin"
    resp = await client.get(url)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_article_with_trailing_slash(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2018/07/let-the-journey-begin/"
    resp = await client.get(url)
    assert resp.status_code == 307
    assert resp.headers["Location"] == (
        "http://florimond.dev/en/posts/2018/07/let-the-journey-begin"
    )


@pytest.mark.asyncio
async def test_tag(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/tag/python"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]

    url = "http://florimond.dev/fr/tag/test"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]
    assert "Tutoriels" in resp.text  # Navbar


@pytest.mark.asyncio
async def test_tag_hx(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/tag/python"
    resp = await client.get(url, headers={"HX-Request": "true"})
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    _, attrs = get_start_tag(resp.text)
    assert attrs["data-testid"] == "post-list"


@pytest.mark.asyncio
async def test_extra_content_dirs(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2020/01/test-draft"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]

    url = "http://florimond.dev/fr/posts/2021/04/test-brouillon"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]
    assert "Tutoriels" in resp.text  # Navbar


@pytest.mark.asyncio
async def test_private_link(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2020/01/test-draft-prv-1"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]
    assert "private link" in resp.text.lower()
    assert "do not share" in resp.text.lower()


KNOWN_CATEGORIES = ["essays", "retrospectives", "tutorials"]


@pytest.mark.asyncio
async def test_known_categories() -> None:
    category_repository = resolve(CategoryRepository)
    categories = await category_repository.find_all()
    assert [c.slug for c in categories] == KNOWN_CATEGORIES


@pytest.mark.asyncio
@pytest.mark.parametrize("category", KNOWN_CATEGORIES)
async def test_category(client: httpx.AsyncClient, category: str) -> None:
    url = f"http://florimond.dev/en/category/{category}"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_category_i18n(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/fr/category/tutorials"
    resp = await client.get(url)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]
    assert "Tutoriels" in resp.text  # Navbar


@pytest.mark.asyncio
async def test_category_hx(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/category/tutorials"
    resp = await client.get(url, headers={"HX-Request": "true"})
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    _, attrs = get_start_tag(resp.text)
    assert attrs["data-testid"] == "post-list"


@pytest.mark.asyncio
async def test_not_found(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/foo"
    resp = await client.get(url, follow_redirects=True)
    assert resp.status_code == 404
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_not_found_article(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2022/06/whatever"
    resp = await client.get(url)
    assert resp.status_code == 404
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_not_found_category(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/category/whatever"
    resp = await client.get(url)
    assert resp.status_code == 404
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_not_found_keyword(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/tag/whatever"
    resp = await client.get(url)
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
    assert 'href="http://florimond.dev/feed.rss"' in line


@pytest.mark.asyncio
async def test_meta(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/en/posts/2018/07/let-the-journey-begin"
    resp = await client.get(url)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]

    meta = find_meta_tags(resp.text)

    def find_meta(typ: str, value: str) -> dict | None:
        for item in meta:
            if item.get(typ) == value:
                return item.get("content")
        return None

    meta_url = "http://florimond.dev/en/posts/2018/07/let-the-journey-begin"
    assert find_meta("name", "description") is not None
    assert find_meta("property", "og:url") == meta_url
    assert find_meta("property", "og:title") is not None
    assert find_meta("property", "og:description") is not None
