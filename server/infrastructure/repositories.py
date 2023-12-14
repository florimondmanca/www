from typing import cast

from .. import i18n
from ..domain.entities import BlogPosting, Category, Keyword, Pagination
from ..domain.repositories import (
    BlogPostingFilterSet,
    BlogPostingRepository,
    CategoryRepository,
    KeywordRepository,
)
from ..i18n import gettext_lazy as _
from .database import InMemoryDatabase


class InMemoryBlogPostingRepository(BlogPostingRepository):
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    async def find_all(
        self, filterset: BlogPostingFilterSet | None = None
    ) -> Pagination[BlogPosting]:
        if filterset is None:
            filterset = BlogPostingFilterSet()

        return self._db.find_all_blog_postings(filterset)

    async def find_by_slug(self, slug: str) -> BlogPosting | None:
        language = i18n.get_locale().language
        return self._db.find_one_blog_posting(language, slug)


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
