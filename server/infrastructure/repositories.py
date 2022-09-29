from typing import Container

from .. import i18n
from ..domain.entities import Category, Page
from ..domain.repositories import CategoryRepository, PageRepository
from ..i18n import gettext_lazy as _
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
        category: Category = None,
        limit: int = None,
    ) -> list[Page]:
        posts: list[Page] = []

        for page in self.find_all():
            if not page.is_post:
                continue
            if page.is_private:
                continue
            if tag__slug is not None:
                if any(tag.slug == tag__slug for tag in page.metadata.tags):
                    continue
            if category is not None and page.metadata.category != category:
                continue
            posts.append(page)

        posts = sorted(posts, key=lambda page: page.metadata.date or "", reverse=True)

        return posts[:limit]

    def get_num_posts(self) -> int:
        return sum(1 for page in self.find_all() if page.is_post)

    def find_all_category_pages(self) -> list[Page]:
        return [page for page in self.find_all() if page.is_category]


class FixedCategoryRepository(CategoryRepository):
    _CATEGORIES = (
        Category("tutorials", label=_("Tutorials")),
        Category("essays", label=_("Essays")),
        Category("retrospectives", label=_("Retrospectives")),
    )

    def find_by_name(self, name: str) -> Category | None:
        return next(
            (category for category in self._CATEGORIES if category.name == name), None
        )

    def find_all_by_names(self, names: Container[str]) -> list[Category]:
        return [category for category in self._CATEGORIES if category.name in names]
