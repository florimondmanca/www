import httpx
import pytest


@pytest.mark.asyncio
async def test_i18n_home(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/fr/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]

    assert "Tutoriels" in resp.text  # Navbar
    assert "Ingénieur logiciel" in resp.text  # Jumbotron
    assert "25 juillet 2018" in resp.text  # Article list

    # Language switch
    assert 'href="http://florimond.dev/fr/"' in resp.text
    assert 'href="http://florimond.dev/en/"' in resp.text


@pytest.mark.asyncio
async def test_i18n_article(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/fr/blog/articles/2018/07/let-the-journey-begin/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]

    # Navbar
    assert "Tutoriels" in resp.text

    # Article meta
    assert "25 juillet 2018" in resp.text

    # TODO: translated content

    # Language switch
    assert (
        'href="http://florimond.dev/fr/blog/articles/2018/07/let-the-journey-begin/"'
        in resp.text
    )
    assert (
        'href="http://florimond.dev/en/blog/articles/2018/07/let-the-journey-begin/"'
        in resp.text
    )


@pytest.mark.asyncio
async def test_i18n_unknown_language(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/de/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 404
    assert "text/html" in resp.headers["content-type"]
