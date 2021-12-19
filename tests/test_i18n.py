import httpx
import pytest

from server.i18n import get_locale, set_locale


@pytest.mark.asyncio
async def test_i18n_home(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/fr/"
    resp = await client.get(url)
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]

    assert f'href="{url}"' in resp.text  # Navbar home link is localized.
    assert "EN" in resp.text and "FR" in resp.text  # Language switch is present.
    assert "Tutoriels" in resp.text  # Navbar categories are localized.


@pytest.mark.asyncio
async def test_i18n_unknown_language(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/de/"
    resp = await client.get(url)
    assert resp.status_code == 404
    assert "text/html" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_i18n_locale() -> None:
    locale = get_locale()
    assert locale.language == "en"
    assert repr(locale) == "<Locale('en')>"

    set_locale("fr")
    locale = get_locale()
    assert locale.language == "fr"
    assert repr(locale) == "<Locale('fr')>"
