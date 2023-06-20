import pytest
from playwright.sync_api import Page, expect

from .util import Server

pytestmark = pytest.mark.skip


def test_e2e_home(server: Server, page: Page) -> None:
    page.goto(server.url)

    expect(page).to_have_title("Florimond Manca")
    expect(page.get_by_role("heading", level=1)).to_have_text("Florimond Manca")


def test_e2e_en_nav(server: Server, page: Page) -> None:
    page.goto(server.url)

    nav = page.get_by_role("navigation")
    links = iter(nav.get_by_role("link").all())

    link = next(links)
    expect(link).to_have_text("Florimond Manca")
    expect(link).to_have_attribute("href", f"{server.url}/en/")

    link = next(links)
    expect(link).to_have_text("Essays")
    expect(link).to_have_attribute("href", "/en/category/essays/")

    link = next(links)
    expect(link).to_have_text("Retrospectives")
    expect(link).to_have_attribute("href", "/en/category/retrospectives/")

    link = next(links)
    expect(link).to_have_text("Tutorials")
    expect(link).to_have_attribute("href", "/en/category/tutorials/")

    link = next(links)
    expect(link).to_have_text("EN")
    expect(link).to_have_attribute("href", f"{server.url}/en/")

    link = next(links)
    expect(link).to_have_text("FR")
    expect(link).to_have_attribute("href", f"{server.url}/fr/")

    with pytest.raises(StopIteration):
        next(links)


def test_e2e_fr_nav(server: Server, page: Page) -> None:
    page.goto(f"{server.url}/fr/")

    nav = page.get_by_role("navigation")
    links = iter(nav.get_by_role("link").all())

    link = next(links)
    expect(link).to_have_text("Florimond Manca")
    expect(link).to_have_attribute("href", f"{server.url}/fr/")

    link = next(links)
    expect(link).to_have_text("Idées")
    expect(link).to_have_attribute("href", "/fr/category/essays/")

    link = next(links)
    expect(link).to_have_text("Rétrospectives")
    expect(link).to_have_attribute("href", "/fr/category/retrospectives/")

    # Present due to test drafts
    link = next(links)
    expect(link).to_have_text("Tutoriels")
    expect(link).to_have_attribute("href", "/fr/category/tutorials/")

    link = next(links)
    expect(link).to_have_text("EN")
    expect(link).to_have_attribute("href", f"{server.url}/en/")

    link = next(links)
    expect(link).to_have_text("FR")
    expect(link).to_have_attribute("href", f"{server.url}/fr/")

    with pytest.raises(StopIteration):
        next(links)
