from .. import i18n
from ..domain.entities import Page
from ..domain.repositories import PageRepository
from .database import PageDatabase


class InMemoryPageRepository(PageRepository):
    def __init__(self, db: PageDatabase) -> None:
        self._db = db

    def find_by_permalink(self, permalink: str) -> Page | None:
        language = i18n.get_locale().language
        return self._db.find_one(language, permalink)

    def find_all(self, language: str = None) -> list[Page]:
        if language is None:
            language = i18n.get_locale().language
        return self._db.find_all(language)

    def find_all_post_pages(
        self,
        *,
        tag__slug: str = None,
        category: str = None,
        limit: int = None,
    ) -> list[Page]:
        posts = []

        for page in self.find_all():
            if not page.is_post:
                continue
            if page.is_private:
                continue
            if tag__slug is not None:
                if any(tag.slug == tag__slug for tag in page.frontmatter.tags):
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
