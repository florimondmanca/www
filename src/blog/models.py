import pathlib
import typing

import sortedcontainers

from .exceptions import DoesNotExist


class Frontmatter(typing.NamedTuple):
    title: str
    description: str
    date: str
    tags: typing.List[str]


class Article(typing.NamedTuple):
    content: str
    permalink: str
    slug: str
    frontmatter: Frontmatter

    def __repr__(self) -> str:
        items = (("title", self.frontmatter.title), ("date", self.frontmatter.date))
        descr = ", ".join(f"{key}={value!r}" for key, value in items)
        return f"<Article {descr}>"


Order = typing.Literal["asc", "desc"]


class Index:
    """
    An in-memory, date-ordered index of articles.
    """

    def __init__(self, root: pathlib.Path) -> None:
        self.root = root
        self._data = sortedcontainers.SortedDict()

    def _all(self, order: Order = "asc") -> typing.Iterator[Article]:
        source = self._data.values()

        if order == "desc":
            source = reversed(source)

        for articles in source:
            for article in articles:
                yield article

    def insert(self, article: Article) -> None:
        for other in self._all():
            if other.slug == article.slug:
                raise RuntimeError(f"Slug {article.slug!r} is not unique")

        key = article.frontmatter.date
        self._data.setdefault(key, [])
        self._data[key].append(article)

    def find_one_or_error(self, key: typing.Callable[[Article], bool]) -> Article:
        for article in self._all():
            if key(article):
                return article
        else:
            raise DoesNotExist

    def find_all(
        self,
        key: typing.Callable[[Article], bool] = lambda article: True,
        order: Order = "asc",
    ) -> typing.Iterator[Article]:
        for article in self._all(order=order):
            if key(article):
                yield article

    def clear(self) -> None:
        self._data.clear()
