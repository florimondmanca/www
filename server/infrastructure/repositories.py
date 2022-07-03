from .. import i18n
from ..domain.entities import Page
from ..domain.repositories import PageRepository


class InMemoryPageRepository(PageRepository):
    def __init__(self) -> None:
        self._store: dict[str, dict[str, Page]] = {}

    def find_by_permalink(self, permalink: str) -> Page | None:
        language = i18n.get_locale().language
        return self._store.get(language, {}).get(permalink)

    def find_all(self, language: str = None) -> list[Page]:
        if language is None:
            language = i18n.get_locale().language
        return list(self._store.get(language, {}).values())

    def find_all_post_pages(
        self,
        *,
        tag: str = None,
        category: str = None,
        limit: int = None,
    ) -> list[Page]:
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

    def find_all_category_pages(self) -> list[Page]:
        return [page for page in self.find_all() if page.is_category]

    def save(self, page: Page) -> None:
        pages = self._store.setdefault(page.language, {})
        pages[page.permalink] = page
