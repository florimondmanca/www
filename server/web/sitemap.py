from typing import List

import asgi_sitemaps

from .. import settings
from ..domain.entities import Page
from ..resources import page_repository


class StaticSitemap(asgi_sitemaps.Sitemap):
    protocol = "https"

    def items(self) -> List[str]:
        return ["/"]

    def location(self, path: str) -> str:
        return path

    def changefreq(self, path: str) -> str:
        return "weekly"


class PagesSitemap(asgi_sitemaps.Sitemap):
    protocol = "https"

    def items(self) -> List[Page]:
        pages = []
        for language in settings.LANGUAGES:
            pages.extend(page_repository.find_all(language))
        return pages

    def location(self, page: Page) -> str:
        return page.permalink

    def changefreq(self, path: str) -> str:
        return "weekly"


sitemap = asgi_sitemaps.SitemapApp(
    [StaticSitemap(), PagesSitemap()], domain="florimond.dev"
)
