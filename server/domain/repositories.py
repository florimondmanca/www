from .entities import Page


class PageRepository:
    def find_by_permalink(self, permalink: str) -> Page | None:
        raise NotImplementedError  # pragma: no cover

    def find_all(self, language: str = None) -> list[Page]:
        raise NotImplementedError  # pragma: no cover

    def find_all_post_pages(
        self, *, tag__slug: str = None, category: str = None, limit: int = None
    ) -> list[Page]:
        raise NotImplementedError  # pragma: no cover

    def find_all_category_pages(self) -> list[Page]:
        raise NotImplementedError  # pragma: no cover
