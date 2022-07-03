import typing

from .. import i18n
from .entities import Page


class PageRepository:
    """
    An in-memory container of pages.
    """

    def __init__(self) -> None:
        self._pages: typing.Dict[str, typing.List[Page]] = {}

    def find_by_permalink(self, permalink: str) -> typing.Optional[Page]:
        for page in self.find_all():
            if page.permalink == permalink:
                return page
        return None

    def find_all(self, language: str = None) -> typing.List[Page]:
        if language is None:
            language = i18n.get_locale().language
        return self._pages[language]

    def find_all_post_pages(
        self,
        *,
        tag: str = None,
        category: str = None,
        limit: int = None,
    ) -> typing.List[Page]:
        posts = []

        for page in self.find_all():
            if not page.is_post:
                continue
            if page.is_private:
                continue
            if tag is not None and tag not in page.frontmatter.tags:
                continue
            if category is not None and page.frontmatter.category != category:
                continue
            posts.append(page)

        posts = sorted(
            posts, key=lambda page: page.frontmatter.date or "", reverse=True
        )

        return posts[:limit]

    def find_all_category_pages(self) -> typing.List[Page]:
        return [page for page in self.find_all() if page.is_category]

    def save(self, pages: typing.Dict[str, typing.List[Page]]) -> None:
        self._pages = pages
