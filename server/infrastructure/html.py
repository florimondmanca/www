from html.parser import HTMLParser

from markupsafe import Markup

from .. import settings
from ..domain.entities import ObjWithMeta
from .urls import get_absolute_path, to_production_url


def build_meta_tags(obj: ObjWithMeta) -> list[dict]:
    url = to_production_url(get_absolute_path(obj))
    title = obj.meta_title
    description = obj.meta_description
    date_published = obj.meta_date_published
    keywords = obj.meta_keywords

    meta_tags: list[dict[str, str | None]] = [
        # General
        dict(name="description", content=description),
        dict(itemprop="name", content=title),
        dict(itemprop="description", content=description),
        # OpenGraph
        dict(property="og:url", content=url),
        dict(property="og:type", content="article"),
        dict(property="og:title", content=title),
        dict(property="og:description", content=description),
        dict(property="og:site_name", content=settings.SITE_TITLE),
        dict(
            property="article:published_time",
            content=date_published.strftime("%Y-%M-%d")
            if date_published is not None
            else None,
        ),
    ]

    for keyword in keywords:
        meta_tags.append(dict(property="article:tag", content=keyword))

    meta_tags = [attrs for attrs in meta_tags if attrs["content"] is not None]

    return meta_tags


class _WebmentionContentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attr = dict(attrs)

        if tag == "a":
            kept_attributes = {"href": attr["href"]}

            if "class" in attr:
                # Allow microformats classes.
                kept_attributes["class"] = attr["class"]

            kept_attr_line = " ".join(
                f'{name}="{value}"' for name, value in kept_attributes.items()
            )

            self._buffer.append(f"<a {Markup(kept_attr_line)}>")
            return

        # In general, drop attributes.
        self._buffer.append(f"<{tag}>")

    def handle_data(self, data: str) -> None:
        self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        self._buffer.append(f"</{tag}>")

    def get_content(self) -> str:
        return "".join(self._buffer)


def escape_webmention_content(value: str) -> str:
    parser = _WebmentionContentParser()
    parser.feed(value)
    return parser.get_content()
