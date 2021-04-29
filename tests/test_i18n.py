import httpx
import pytest

from server.i18n import get_locale, set_locale


@pytest.mark.asyncio
async def test_i18n_home(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/fr/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]

    assert "Tutoriels" in resp.text  # Navbar


@pytest.mark.asyncio
async def test_i18n_unknown_language(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/de/"
    resp = await client.get(url, allow_redirects=False)
    assert resp.status_code == 404
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_i18n_locale() -> None:
    locale = get_locale()
    assert locale.language == "en"
    assert repr(locale) == "Locale('en')"

    set_locale("fr")
    locale = get_locale()
    assert repr(locale) == "Locale('fr')"
