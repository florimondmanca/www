from contextlib import contextmanager
from typing import Iterator

import aiofiles

from ..domain.entities import BlogPosting, Category, Keyword
from .content import aiter_blog_posting_paths, build_blog_posting


class _Data:
    def __init__(self) -> None:
        self.blog_postings: dict[str, dict[str, BlogPosting]] = {}
        self.categories: dict[str, dict[str, Category]] = {}
        self.keywords: dict[str, dict[str, Keyword]] = {}


class InMemoryDatabase:
    def __init__(self) -> None:
        self._data = _Data()

    async def connect(self) -> None:
        await self._load()

    async def reload(self) -> None:
        await self._load()  # pragma: no cover

    @contextmanager
    def isolated(self) -> Iterator[None]:
        previous_data = self._data
        self._data = _Data()
        try:
            yield
        finally:
            self._data = previous_data

    async def _load(self) -> None:
        self._data = _Data()

        async for root, path in aiter_blog_posting_paths():
            async with aiofiles.open(path) as f:
                raw = await f.read()

            blog_posting = await build_blog_posting(root, path, raw)

            self._data.blog_postings.setdefault(blog_posting.in_language, {})
            self._data.blog_postings[blog_posting.in_language][
                blog_posting.slug
            ] = blog_posting

    def find_all_blog_postings(self, language: str) -> list[BlogPosting]:
        return sorted(
            self._data.blog_postings.get(language, {}).values(),
            key=lambda blog_posting: blog_posting.date_published,
            reverse=True,
        )

    def find_one_blog_posting(self, language: str, slug: str) -> BlogPosting | None:
        return self._data.blog_postings.get(language, {}).get(slug)

    def find_all_categories(self, language: str) -> list[Category]:
        return sorted(
            self._data.categories.get(language, {}).values(),
            key=lambda category: category.slug,
        )

    def find_one_category(self, language: str, slug: str) -> Category | None:
        return self._data.categories.get(language, {}).get(slug)

    def insert_category(self, category: Category) -> None:
        self._data.categories.setdefault(category.in_language, {})
        self._data.categories[category.in_language][category.slug] = category

    def find_all_keywords(self, language: str) -> list[Keyword]:
        return sorted(
            self._data.keywords.get(language, {}).values(),
            key=lambda keyword: keyword.name,
        )

    def find_one_keyword(self, language: str, name: str) -> Keyword | None:
        return self._data.keywords.get(language, {}).get(name)

    def insert_keyword(self, keyword: Keyword) -> None:
        self._data.keywords.setdefault(keyword.in_language, {})
        self._data.keywords[keyword.in_language][keyword.name] = keyword
