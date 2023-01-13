from typing import List

import asgi_sitemaps

from .. import settings
from ..di import resolve
from ..domain.entities import BlogPosting, Category, Keyword
from ..domain.repositories import (
    BlogPostingRepository,
    CategoryRepository,
    KeywordRepository,
)
from ..infrastructure.urls import get_absolute_url


class StaticSitemap(asgi_sitemaps.Sitemap):
    protocol = "https"

    def items(self) -> List[str]:
        return ["/"]

    def location(self, path: str) -> str:
        return path

    def changefreq(self, path: str) -> str:
        return "weekly"


class BlogPostingSitemap(asgi_sitemaps.Sitemap):
    protocol = "https"

    async def items(self) -> List[BlogPosting]:
        repository = resolve(BlogPostingRepository)
        return [
            obj
            for language in settings.LANGUAGES
            for obj in await repository.find_all(language)
        ]

    def location(self, blog_posting: BlogPosting) -> str:
        return get_absolute_url(blog_posting)

    def changefreq(self, path: str) -> str:
        return "weekly"


class CategorySitemap(asgi_sitemaps.Sitemap):
    protocol = "https"

    async def items(self) -> List[Category]:
        repository = resolve(CategoryRepository)
        return [
            obj
            for language in settings.LANGUAGES
            for obj in await repository.find_all(language)
        ]

    def location(self, obj: Category) -> str:
        return get_absolute_url(obj)

    def changefreq(self, path: str) -> str:
        return "weekly"


class KeywordSitemap(asgi_sitemaps.Sitemap):
    protocol = "https"

    async def items(self) -> List[Keyword]:
        repository = resolve(KeywordRepository)
        return [
            obj
            for language in settings.LANGUAGES
            for obj in await repository.find_all(language)
        ]

    def location(self, obj: Keyword) -> str:
        return get_absolute_url(obj)

    def changefreq(self, path: str) -> str:
        return "weekly"


sitemap = asgi_sitemaps.SitemapApp(
    [StaticSitemap(), BlogPostingSitemap(), CategorySitemap(), KeywordSitemap()],
    domain="florimond.dev",
)
