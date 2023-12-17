from typing import List

import asgi_sitemaps

from .. import settings
from ..di import resolve
from ..domain.entities import Category, Keyword, Post
from ..domain.repositories import (
    CategoryRepository,
    KeywordRepository,
    PostFilterSet,
    PostRepository,
)
from ..infrastructure.urls import get_absolute_path


class StaticSitemap(asgi_sitemaps.Sitemap):
    protocol = "https"

    def items(self) -> List[str]:
        return ["/"]

    def location(self, path: str) -> str:
        return path

    def changefreq(self, path: str) -> str:
        return "weekly"


class PostSitemap(asgi_sitemaps.Sitemap):
    protocol = "https"

    async def items(self) -> List[Post]:
        repository = resolve(PostRepository)
        return [
            obj
            for language in settings.LANGUAGES
            for obj in (
                await repository.find_all(PostFilterSet(page=None, language=language))
            ).items
        ]

    def location(self, post: Post) -> str:
        return get_absolute_path(post)

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
        return get_absolute_path(obj)

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
        return get_absolute_path(obj)

    def changefreq(self, path: str) -> str:
        return "weekly"


sitemap = asgi_sitemaps.SitemapApp(
    [StaticSitemap(), PostSitemap(), CategorySitemap(), KeywordSitemap()],
    domain="florimond.dev",
)
