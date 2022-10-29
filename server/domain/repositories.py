from .entities import BlogPosting, Category, Keyword


class BlogPostingRepository:
    async def find_all(self, language: str = None) -> list[BlogPosting]:
        raise NotImplementedError  # pragma: no cover

    async def find_all_by_category(self, category: Category) -> list[BlogPosting]:
        raise NotImplementedError  # pragma: no cover

    async def find_all_by_keyword(self, keyword: Keyword) -> list[BlogPosting]:
        raise NotImplementedError  # pragma: no cover

    async def find_by_slug(self, slug: str) -> BlogPosting | None:
        raise NotImplementedError  # pragma: no cover


class CategoryRepository:
    def make_name(self, slug: str, language: str) -> str:
        raise NotImplementedError  # pragma: no cover

    async def find_all(self, language: str = None) -> list[Category]:
        raise NotImplementedError  # pragma: no cover

    async def find_by_slug(self, slug: str, language: str = None) -> Category | None:
        raise NotImplementedError  # pragma: no cover

    async def save(self, category: Category) -> None:
        raise NotImplementedError  # pragma: no cover


class KeywordRepository:
    async def find_all(self, language: str) -> list[Keyword]:
        raise NotImplementedError  # pragma: no cover

    async def find_by_name(self, name: str, language: str = None) -> Keyword | None:
        raise NotImplementedError  # pragma: no cover

    async def save(self, keyword: Keyword) -> None:
        raise NotImplementedError  # pragma: no cover
