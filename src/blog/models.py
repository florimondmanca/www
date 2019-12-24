import typing


class Frontmatter(typing.NamedTuple):
    title: str
    description: typing.Optional[str] = None
    home: bool = False
    date: typing.Optional[str] = None
    image: typing.Optional[str] = None
    image_caption: typing.Optional[str] = None
    tags: typing.List[str] = []
    tag: typing.Optional[str] = None


class Page(typing.NamedTuple):
    permalink: str
    frontmatter: Frontmatter
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

        return sorted(articles, key=lambda page: page.frontmatter.date, reverse=True)
