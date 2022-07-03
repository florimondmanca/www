import typing

from .entities import Page


class PageRepository:
    def find_by_permalink(self, permalink: str) -> typing.Optional[Page]:
        raise NotImplementedError  # pragma: no cover

    def find_all(self, language: str = None) -> typing.List[Page]:
        raise NotImplementedError  # pragma: no cover

    def find_all_post_pages(
        self,
        *,
        tag: str = None,
        category: str = None,
        limit: int = None,
    ) -> typing.List[Page]:
        raise NotImplementedError  # pragma: no cover

    def find_all_category_pages(self) -> typing.List[Page]:
        raise NotImplementedError  # pragma: no cover

    def save(self, page: Page) -> None:
        raise NotImplementedError  # pragma: no cover
