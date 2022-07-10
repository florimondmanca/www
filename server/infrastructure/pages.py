from pathlib import Path
from typing import Any, Iterable

from .. import settings
from ..domain.entities import Frontmatter, Page, Tag
from ..i18n import get_locale
from ..i18n import gettext_lazy as _
from .adapters import frontmatter as fm
from .adapters import markdown
from .filesystem import ContentItem
from .urls import to_production_url


def build_pages(items: list[ContentItem]) -> list[Page]:
    pages = _build_content_pages(items)

    tags = {tag for page in pages for tag in page.frontmatter.tags}
    pages.extend(_build_tag_pages(tags))

    categories = sorted(
        {
            page.frontmatter.category
            for page in pages
            if page.frontmatter.category is not None
        },
        key=list(_CATEGORY_LABELS).index,
    )
    pages.extend(_build_category_pages(categories))

    return pages


def _build_content_pages(items: list[ContentItem]) -> list[Page]:
    pages = []

    for item in items:
        content, attrs = fm.decode(item.content)
        html = markdown.render(content)
        permalink = _build_permalink(item.location)
        image, image_thumbnail = _process_image(attrs)
        frontmatter = Frontmatter(
            title=attrs["title"],
            description=attrs.get("description"),
            category=attrs.get("category"),
            date=attrs.get("date"),
            image=image,
            image_thumbnail=image_thumbnail,
            image_caption=attrs.get("image_caption"),
            tags=[Tag(slug) for slug in attrs.get("tags", [])],
        )
        meta = _build_meta(permalink, frontmatter)

        page = Page(
            html=html,
            content=content,
            permalink=permalink,
            frontmatter=frontmatter,
            meta=meta,
        )

        pages.append(page)

    return pages


def _build_tag_pages(tags: Iterable[Tag]) -> list[Page]:
    language = get_locale().language
    tag_pages = []

    for tag in tags:
        frontmatter = Frontmatter(
            title=f"{tag.slug} - {settings.SITE_TITLE}",
            description=f"Posts about #{tag}",
            tag=tag,
        )
        permalink = f"/{language}/tag/{tag}"
        meta = _build_meta(permalink, frontmatter)
        page = Page(permalink=permalink, frontmatter=frontmatter, meta=meta)
        tag_pages.append(page)

    return tag_pages


def _build_category_pages(categories: Iterable[str]) -> list[Page]:
    language = get_locale().language
    pages = []

    for category in categories:
        label = get_category_label(category)
        frontmatter = Frontmatter(
            title=f"{label} - {settings.SITE_TITLE}",
            description=label,
            category=category,
        )
        permalink = f"/{language}/category/{category}"
        meta = _build_meta(permalink, frontmatter)
        page = Page(permalink=permalink, frontmatter=frontmatter, meta=meta)
        pages.append(page)

    return pages


def _build_permalink(location: Path) -> str:
    assert location.suffix == ".md"
    assert not location.is_absolute()
    segments = location.with_suffix("").parts
    assert segments
    return "/" + "/".join(segments)


def _process_image(attrs: dict[str, Any]) -> tuple[str | None, str | None]:
    image = attrs.get("image")
    image_thumbnail = attrs.get("image_thumbnail")

    is_image_self_hosted = isinstance(image, str) and image.startswith(
        settings.STATIC_ROOT
    )

    if image_thumbnail is None and is_image_self_hosted:
        # By default, use the same image
        image_thumbnail = image

    if image_thumbnail == "__auto__":
        # Convention: '/static/example.jpg' -> '/static/example_thumbnail.jpg'
        if is_image_self_hosted:
            assert isinstance(image, str)
            image_thumbnail = _append_filename(image, "_thumbnail")
        else:
            image_thumbnail = None

    assert image is None or isinstance(image, str)
    assert image_thumbnail is None or isinstance(image_thumbnail, str)

    return image, image_thumbnail


def _append_filename(filename: str, suffix: str) -> str:
    path = Path(filename)
    name = f"{path.stem}{suffix}{path.suffix}"
    return str(path.with_name(name))


def _build_meta(permalink: str, frontmatter: Frontmatter) -> list[dict]:
    path = permalink + ("" if permalink.endswith("/") else "/")
    url = to_production_url(path)

    image_url = frontmatter.image
    if image_url:
        image_url = to_production_url(image_url)

    meta: list[dict[str, str | None]] = [
        # General
        dict(name="description", content=frontmatter.description),
        dict(name="image", content=image_url),
        dict(itemprop="name", content=frontmatter.title),
        dict(itemprop="description", content=frontmatter.description),
        # Twitter
        dict(name="twitter:url", content=url),
        dict(name="twitter:title", content=frontmatter.title),
        dict(name="twitter:description", content=frontmatter.description),
        dict(name="twitter:image", content=image_url),
        dict(name="twitter:card", content="summary_large_image"),
        dict(name="twitter:site", content="@florimondmanca"),
        # OpenGraph
        dict(property="og:url", content=url),
        dict(property="og:type", content="article"),
        dict(property="og:title", content=frontmatter.title),
        dict(property="og:description", content=frontmatter.description),
        dict(property="og:image", content=image_url),
        dict(property="og:site_name", content=settings.SITE_TITLE),
        dict(property="article:published_time", content=frontmatter.date),
    ]

    for tag in frontmatter.tags:
        meta.append(dict(property="article:tag", content=tag.slug))

    return meta


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
