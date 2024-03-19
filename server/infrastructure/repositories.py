import time
from typing import cast

import httpx

from .. import i18n
from ..domain.entities import Category, Keyword, Pagination, Post
from ..domain.repositories import (
    CategoryRepository,
    KeywordRepository,
    PostFilterSet,
    PostRepository,
    Webmention,
    WebmentionRepository,
)
from ..i18n import gettext_lazy as _
from .database import InMemoryDatabase
from .urls import get_absolute_path


class InMemoryPostRepository(PostRepository):
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    async def find_all(
        self, filterset: PostFilterSet | None = None
    ) -> Pagination[Post]:
        if filterset is None:
            filterset = PostFilterSet()

        return self._db.find_all_posts(filterset)

    async def find_by_slug(self, slug: str) -> Post | None:
        language = i18n.get_locale().language
        return self._db.find_one_post(language, slug)


class InMemoryCategoryRepository(CategoryRepository):
    _NAMES = {
        "essays": {
            "en": "Essays",
            "fr": _("Essays"),
        },
        "retrospectives": {
            "en": "Retrospectives",
            "fr": _("Retrospectives"),
        },
        "tutorials": {
            "en": "Tutorials",
            "fr": _("Tutorials"),
        },
    }

    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    def make_name(self, slug: str, language: str) -> str:
        return cast(str, self._NAMES[slug][language])

    async def find_all(self, language: str | None = None) -> list[Category]:
        if language is None:
            language = i18n.get_locale().language
        return self._db.find_all_categories(language)

    async def find_by_slug(
        self, slug: str, language: str | None = None
    ) -> Category | None:
        if language is None:
            language = i18n.get_locale().language
        return self._db.find_one_category(language, slug)

    async def save(self, category: Category) -> None:
        self._db.insert_category(category)


class InMemoryKeywordRepository(KeywordRepository):
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    async def find_all(self, language: str) -> list[Keyword]:
        return self._db.find_all_keywords(language)

    async def find_by_name(
        self, name: str, language: str | None = None
    ) -> Keyword | None:
        if language is None:
            language = i18n.get_locale().language
        return self._db.find_one_keyword(language, name)

    async def save(self, keyword: Keyword) -> None:
        self._db.insert_keyword(keyword)


class WebmentionIOWebmentionRepository(WebmentionRepository):
    def __init__(
        self,
        client: httpx.AsyncClient,
        ttl: int | float = float("inf"),
    ) -> None:
        self._client = client
        self._data: dict | None = None
        self._ttl = ttl
        self._last_fetch: float | None = None

    async def find_for_post(self, post: Post) -> list[Webmention]:
        post_url = f"https://florimond.dev{get_absolute_path(post)}"

        if self._data is None or (
            self._last_fetch is not None and time.time() > self._last_fetch + self._ttl
        ):
            url = "https://webmention.io/api/mentions.jf2"
            response = await self._client.request(
                "GET", url, params={"target": post_url}
            )
            self._data = response.json()
            self._last_fetch = time.time()

        assert self._data is not None

        webmentions = []

        for child in self._data["children"]:
            if child["type"] == "entry" and child.get("in-reply-to") == post_url:
                webmentions.append(Webmention(data=child))

        return webmentions
