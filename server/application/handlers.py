from pathlib import Path
from typing import Iterable

from .. import settings
from ..di import resolve
from ..domain.entities import Category, Metadata, Page, Tag
from ..domain.repositories import CategoryRepository
from ..i18n import get_locale
from .parsers import Parser
from .queries import GetPages
from .sources import ContentItem


async def get_pages(query: GetPages) -> list[Page]:
    category_repository = resolve(CategoryRepository)

    pages = await _build_content_pages(query.items)

    tags = {tag for page in pages for tag in page.metadata.tags}
    pages.extend(_build_tag_pages(tags))

    categories = category_repository.find_all_by_names(
        {c.name for page in pages if (c := page.metadata.category) is not None}
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


def _build_category_pages(categories: Iterable[Category]) -> list[Page]:
    language = get_locale().language
    pages = []

    for category in categories:
        metadata = Metadata(
            title=f"{category.label} - {settings.SITE_TITLE}",
            description=category.label,
            category=category,
        )
        permalink = f"/{language}/category/{category.name}"
        page = Page(permalink=permalink, metadata=metadata)
        pages.append(page)

    return pages


def _build_permalink(location: Path) -> str:
    assert location.suffix == ".md"
    assert not location.is_absolute()
    segments = location.with_suffix("").parts
    assert segments
    return "/" + "/".join(segments)
