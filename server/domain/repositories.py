from dataclasses import dataclass, field

from .. import i18n
from .entities import BlogPosting, Category, Keyword, Page, Pagination


@dataclass
class BlogPostingFilterSet:
    page: Page | None = field(default_factory=Page)
    language: str = field(default_factory=lambda: i18n.get_locale().language)
    category: Category | None = None
    keyword: Keyword | None = None


class BlogPostingRepository:
    async def find_all(
        self, filterset: BlogPostingFilterSet | None = None
    ) -> Pagination[BlogPosting]:
        raise NotImplementedError  # pragma: no cover

    async def find_by_slug(self, slug: str) -> BlogPosting | None:
        raise NotImplementedError  # pragma: no cover


class CategoryRepository:
    def make_name(self, slug: str, language: str) -> str:
        raise NotImplementedError  # pragma: no cover

    async def find_all(self, language: str | None = None) -> list[Category]:
        raise NotImplementedError  # pragma: no cover

    async def find_by_slug(
        self, slug: str, language: str | None = None
    ) -> Category | None:
        raise NotImplementedError  # pragma: no cover

    async def save(self, category: Category) -> None:
        raise NotImplementedError  # pragma: no cover


class KeywordRepository:
    async def find_all(self, language: str) -> list[Keyword]:
        raise NotImplementedError  # pragma: no cover

    async def find_by_name(
        self, name: str, language: str | None = None
    ) -> Keyword | None:
        raise NotImplementedError  # pragma: no cover

    async def save(self, keyword: Keyword) -> None:
        raise NotImplementedError  # pragma: no cover
