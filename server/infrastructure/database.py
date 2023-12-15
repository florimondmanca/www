import math
from contextlib import contextmanager
from typing import Iterator

import aiofiles

from server.domain.repositories import PostFilterSet

from ..domain.entities import Category, Keyword, Pagination, Post
from .content import aiter_post_paths, build_post


class _Data:
    def __init__(self) -> None:
        self.posts: dict[str, dict[str, Post]] = {}
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

        async for root, path in aiter_post_paths():
            async with aiofiles.open(path) as f:
                raw = await f.read()

            post = await build_post(root, path, raw)

            self._data.posts.setdefault(post.in_language, {})
            self._data.posts[post.in_language][post.slug] = post

    def find_all_posts(self, filterset: PostFilterSet) -> Pagination[Post]:
        language = filterset.language

        items_it = (
            item
            for item in self._data.posts.get(language, {}).values()
            if not item.is_private
        )

        if filterset.category is not None:
            items_it = (
                item for item in items_it if item.category == filterset.category
            )

        if filterset.keyword is not None:
            items_it = (item for item in items_it if filterset.keyword in item.keywords)

        items = list(items_it)
        total_items = len(items)

        items = sorted(
            items,
            key=lambda post: post.date_published,
            reverse=True,
        )

        if filterset.page is not None:
            page_number = filterset.page.number
            page_size = filterset.page.size
            limit = page_size
            offset = page_size * (page_number - 1)
            items = items[offset : offset + limit]
            total_pages = math.ceil(total_items / page_size)
        else:
            page_number = 1
            total_pages = 1
            page_size = total_items

        return Pagination(
            items=items,
            total_items=total_items,
            page_number=page_number,
            page_size=page_size,
            total_pages=total_pages,
        )

    def find_one_post(self, language: str, slug: str) -> Post | None:
        return self._data.posts.get(language, {}).get(slug)

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
