from typing import Container

from .entities import Category, Page


class PageRepository:
    def find_by_permalink(self, permalink: str) -> Page | None:
        raise NotImplementedError  # pragma: no cover

    def find_all(self, language: str = None) -> list[Page]:
        raise NotImplementedError  # pragma: no cover

    def find_all_post_pages(
        self, *, tag__slug: str = None, category: Category = None, limit: int = None
    ) -> list[Page]:
        raise NotImplementedError  # pragma: no cover

    def find_all_category_pages(self) -> list[Page]:
        raise NotImplementedError  # pragma: no cover


class CategoryRepository:
    def find_by_name(self, name: str) -> Category | None:
        raise NotImplementedError  # pragma: no cover

    def find_all_by_names(self, names: Container[str]) -> list[Category]:
        raise NotImplementedError  # pragma: no cover
