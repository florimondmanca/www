from typing import List

import asgi_sitemaps

from .models import Page
from .resources import index


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
        return index.get_pages()

    def location(self, page: Page) -> str:
        return f"/blog{page.permalink}"

    def changefreq(self, path: str) -> str:
        return "weekly"


sitemap = asgi_sitemaps.SitemapApp(
    [StaticSitemap(), PagesSitemap()], domain="florimond.dev"
)
