import pathlib
import typing

from .exceptions import DoesNotExist


class Frontmatter(typing.NamedTuple):
    title: str
    description: typing.Optional[str] = None
    home: bool = False
    date: typing.Optional[str] = None
    tags: typing.List[str] = []
    tag: typing.Optional[str] = None


class Page(typing.NamedTuple):
    permalink: str
    frontmatter: Frontmatter
    content: str = ""


class Index:
    """
    An in-memory container of pages.
    """

    def __init__(self, root: pathlib.Path) -> None:
        self.root = root
        self._pages: typing.List[Page] = []

    def insert(self, page: Page) -> None:
        for other in self._pages:
            if other.permalink == page.permalink:
                raise RuntimeError(f"Permalink {page.permalink!r} is not unique")
        self._pages.append(page)

    def find_one_or_error(self, *, permalink: str) -> Page:
        for page in self._pages:
            if page.permalink.rstrip("/") == permalink.rstrip("/"):
                return page
        else:
            raise DoesNotExist

    def find_all(
        self, condition: typing.Callable[[Page], bool] = lambda page: True,
    ) -> typing.Iterator[Page]:
        for page in self._pages:
            if condition(page):
                yield page

    def clear(self) -> None:
        self._pages.clear()

    def __repr__(self) -> str:
        return f"<Index ({len(self._pages)} pages)>"
