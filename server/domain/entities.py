import dataclasses
import datetime as dt
import re
from dataclasses import dataclass
from typing import Generic, TypeVar

from .. import settings
from ..i18n import gettext_lazy as _

T = TypeVar("T")

PRIVATE_RE = re.compile(r"prv-\d+$")


class ObjWithMeta:
    @property
    def meta_title(self) -> str:
        raise NotImplementedError  # pragma: no cover

    @property
    def meta_description(self) -> str:
        raise NotImplementedError  # pragma: no cover

    @property
    def meta_date_published(self) -> dt.date | None:
        return None

    @property
    def meta_keywords(self) -> list[str]:
        return []


@dataclasses.dataclass(frozen=True)
class Category(ObjWithMeta):
    # https://schema.org/Thing
    name: str
    slug: str
    in_language: str

    @property
    def meta_title(self) -> str:
        return f"{self.name} - {settings.SITE_TITLE}"

    @property
    def meta_description(self) -> str:
        return _("Posts in category '%s'") % self.name


@dataclass(frozen=True)
class Keyword(ObjWithMeta):
    # https://schema.org/Thing
    name: str
    in_language: str

    @property
    def slug(self) -> str:
        return self.name

    @property
    def meta_title(self) -> str:
        return f"{self.name} - {settings.SITE_TITLE}"

    @property
    def meta_description(self) -> str:
        return _("Posts with tag '%s'") % self.name


@dataclasses.dataclass(frozen=True)
class Post(ObjWithMeta):
    # https://schema.org/BlogPosting
    name: str
    abstract: str
    text: str
    slug: str
    edit_url: str
    date_published: dt.date
    category: Category
    in_language: str
    keywords: list[Keyword] = dataclasses.field(default_factory=list)

    @property
    def is_private(self) -> bool:
        return PRIVATE_RE.search(self.slug) is not None

    @property
    def meta_title(self) -> str:
        return f"{self.name} - {settings.SITE_TITLE}"

    @property
    def meta_description(self) -> str:
        return self.abstract

    @property
    def meta_date_published(self) -> dt.date:
        return self.date_published

    @property
    def meta_keywords(self) -> list[str]:
        return [keyword.name for keyword in self.keywords]


@dataclasses.dataclass(frozen=True)
class Page:
    number: int = 1
    size: int = 10


@dataclasses.dataclass(frozen=True)
class Pagination(Generic[T]):
    items: list[T]
    total_items: int
    page_number: int
    page_size: int
    total_pages: int
