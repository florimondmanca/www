import dataclasses
import typing


@dataclasses.dataclass(frozen=True)
class ContentItem:
    content: str
    location: str


@dataclasses.dataclass(frozen=True)
class Frontmatter:
    title: str
    description: typing.Optional[str] = None
    date: typing.Optional[str] = None
    image: typing.Optional[str] = None
    image_thumbnail: typing.Optional[str] = None
    image_caption: typing.Optional[str] = None
    tags: typing.List[str] = dataclasses.field(default_factory=list)
    home: bool = False
    tag: typing.Optional[str] = None


@dataclasses.dataclass(frozen=True)
class Page:
    permalink: str
    frontmatter: Frontmatter
    meta: typing.List["MetaTag"]
    html: str = ""

    @property
    def is_article(self) -> bool:
        return self.permalink.startswith("/articles/")


class Index:
    """
    An in-memory container of pages.
    """

    def __init__(self) -> None:
        self.pages: typing.List[Page] = []

    def articles_by_date(self, *, tag: str = None) -> typing.List[Page]:
        articles = []

        for page in self.pages:
            if not page.is_article:
                continue
            if tag is not None and tag not in page.frontmatter.tags:
                continue
            articles.append(page)

        return sorted(
            articles, key=lambda page: page.frontmatter.date or "", reverse=True
        )


class MetaTag:
    def __init__(self, **attributes: typing.Optional[str]) -> None:
        self.attributes = attributes

    def __str__(self) -> str:
        attrs = " ".join(
            f'{key}="{value}"' for key, value in self.attributes.items() if value
        )
        return f"<meta {attrs}>"
