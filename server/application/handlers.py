from pathlib import Path
from typing import Iterable

from .. import settings
from ..di import resolve
from ..domain.entities import Metadata, Page, Tag
from ..i18n import get_locale
from ..i18n import gettext_lazy as _
from .parsers import Parser
from .queries import GetPages
from .sources import ContentItem


async def get_pages(query: GetPages) -> list[Page]:
    pages = await _build_content_pages(query.items)

    tags = {tag for page in pages for tag in page.metadata.tags}
    pages.extend(_build_tag_pages(tags))

    categories = sorted(
        {
            page.metadata.category
            for page in pages
            if page.metadata.category is not None
        },
        key=list(_CATEGORY_LABELS).index,
    )
    pages.extend(_build_category_pages(categories))

    return pages


async def _build_content_pages(items: list[ContentItem]) -> list[Page]:
    parser = resolve(Parser)

    pages = []

    for item in items:
        content = await item.source.get()
        html, metadata = parser.parse(content)

        permalink = _build_permalink(item.location)
        page = Page(
            html=html,
            permalink=permalink,
            metadata=metadata,
        )
        pages.append(page)

    return pages


def _build_tag_pages(tags: Iterable[Tag]) -> list[Page]:
    language = get_locale().language
    tag_pages = []

    for tag in tags:
        metadata = Metadata(
            title=f"{tag.slug} - {settings.SITE_TITLE}",
            description=f"Posts about #{tag}",
            tag=tag,
        )
        permalink = f"/{language}/tag/{tag}"
        page = Page(permalink=permalink, metadata=metadata)
        tag_pages.append(page)

    return tag_pages


def _build_category_pages(categories: Iterable[str]) -> list[Page]:
    language = get_locale().language
    pages = []

    for category in categories:
        label = get_category_label(category)
        metadata = Metadata(
            title=f"{label} - {settings.SITE_TITLE}",
            description=label,
            category=category,
        )
        permalink = f"/{language}/category/{category}"
        page = Page(permalink=permalink, metadata=metadata)
        pages.append(page)

    return pages


def _build_permalink(location: Path) -> str:
    assert location.suffix == ".md"
    assert not location.is_absolute()
    segments = location.with_suffix("").parts
    assert segments
    return "/" + "/".join(segments)


# TODO: make this use a proper Category entity or something.

_CATEGORY_LABELS = {
    "tutorials": _("Tutorials"),
    "essays": _("Essays"),
    "retrospectives": _("Retrospectives"),
}


def get_category_label(value: str) -> str:
    try:
        return str(_CATEGORY_LABELS[value])
    except KeyError:
        raise ValueError(
            f"Unknown category value: {value!r} (available: {list(_CATEGORY_LABELS)})"
        )
