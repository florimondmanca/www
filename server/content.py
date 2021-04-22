import glob
from pathlib import Path
from typing import Any, AsyncIterator, Dict, Iterable, Iterator, List, Optional, Tuple

import aiofiles
import frontmatter as fm

from . import resources, settings
from .i18n import gettext_lazy as _
from .models import ContentItem, Frontmatter, MetaTag, Page
from .utils import to_production_url


async def load_content() -> None:
    items = [item async for item in load_content_items()]
    resources.index.pages = build_pages(items)


def iter_content_paths() -> Iterator[Tuple[Path, Path]]:
    content_dirs = [settings.CONTENT_DIR, *settings.EXTRA_CONTENT_DIRS]
    for root in content_dirs:
        pattern = str(root / "**" / "*.md")
        for path in glob.glob(pattern, recursive=True):
            yield root, Path(path)


async def load_content_items() -> AsyncIterator[ContentItem]:
    for root, path in iter_content_paths():
        async with aiofiles.open(path) as f:
            content = await f.read()
            yield ContentItem(
                content=content,
                location=str(path.relative_to(root)),
            )


def build_pages(items: List[ContentItem]) -> List[Page]:
    pages = []

    for page in _build_content_pages(items):
        pages.append(page)

    unique_tags = {tag for page in pages for tag in page.frontmatter.tags}

    for page in _generate_tag_pages(unique_tags):
        pages.append(page)

    unique_categories = sorted(
        {
            page.frontmatter.category
            for page in pages
            if page.frontmatter.category is not None
        },
        key=list(_CATEGORY_LABELS).index,
    )
    pages.extend(_generate_category_pages(unique_categories))

    return pages


def _build_content_pages(items: List[ContentItem]) -> Iterator[Page]:
    for item in items:
        post = fm.loads(item.content)
        content = post.content
        html = resources.markdown.reset().convert(content)
        permalink = _build_permalink(item.location)
        image, image_thumbnail = _process_image(post)
        frontmatter = Frontmatter(
            title=post["title"],
            description=post.get("description"),
            category=post.get("category"),
            date=post.get("date"),
            image=image,
            image_thumbnail=image_thumbnail,
            image_caption=post.get("image_caption"),
            tags=post.get("tags", []),
        )
        meta = _build_meta(permalink, frontmatter)

        yield Page(
            html=html,
            content=content,
            permalink=permalink,
            frontmatter=frontmatter,
            meta=meta,
        )


def _process_image(post: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    image = post.get("image")
    image_thumbnail = post.get("image_thumbnail")

    if (
        isinstance(image, str)
        and image.startswith(settings.STATIC_ROOT)
        and image_thumbnail is None
    ):
        # Convention: '/static/example.jpg' -> '/static/example_thumbnail.jpg'
        # May not exist, but we'll handle this error case in HTML.
        image_thumbnail = _append_filename(image, "_thumbnail")

    assert image is None or isinstance(image, str)
    assert image_thumbnail is None or isinstance(image_thumbnail, str)

    return image, image_thumbnail


def _append_filename(filename: str, suffix: str) -> str:
    path = Path(filename)
    name = f"{path.stem}{suffix}{path.suffix}"
    return str(path.with_name(name))


def _generate_tag_pages(tags: Iterable[str]) -> Iterator[Page]:
    for tag in tags:
        frontmatter = Frontmatter(
            title=f"{tag.capitalize()} - Florimond Manca",
            description=f"Articles about #{tag}",
            tag=tag,
        )
        permalink = f"/tag/{tag}"
        meta = _build_meta(permalink, frontmatter)

        yield Page(permalink=permalink, frontmatter=frontmatter, meta=meta)


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


def _generate_category_pages(categories: Iterable[str]) -> Iterator[Page]:
    for category in categories:
        label = get_category_label(category)
        frontmatter = Frontmatter(
            title=f"{label} - Florimond Manca",
            description=label,
            category=category,
        )
        permalink = f"/category/{category}"
        meta = _build_meta(permalink, frontmatter)

        yield Page(permalink=permalink, frontmatter=frontmatter, meta=meta)


def _build_permalink(location: str) -> str:
    url, _, extension = location.partition(".")
    assert extension == "md"

    segments = url.split("/")
    assert segments

    return "/" + "/".join(segments)


def _build_meta(permalink: str, frontmatter: Frontmatter) -> List["MetaTag"]:
    url = f"https://florimond.dev/blog{permalink}"

    image_url = frontmatter.image
    if image_url:
        image_url = to_production_url(image_url)

    meta = [
        # General
        MetaTag(name="description", content=frontmatter.description),
        MetaTag(name="image", content=image_url),
        MetaTag(itemprop="name", content=frontmatter.title),
        MetaTag(itemprop="description", content=frontmatter.description),
        # Twitter
        MetaTag(name="twitter:url", content=url),
        MetaTag(name="twitter:title", content=frontmatter.title),
        MetaTag(name="twitter:description", content=frontmatter.description),
        MetaTag(name="twitter:image", content=image_url),
        MetaTag(name="twitter:card", content="summary_large_image"),
        MetaTag(name="twitter:site", content="@florimondmanca"),
        # OpenGraph
        MetaTag(name="og:url", content=url),
        MetaTag(property="og:type", content="article"),
        MetaTag(property="og:title", content=frontmatter.title),
        MetaTag(property="og:description", content=frontmatter.description),
        MetaTag(property="og:image", content=image_url),
        MetaTag(property="og:site_name", content="Florimond Manca"),
        MetaTag(property="article:published_time", content=frontmatter.date),
    ]

    for tag in frontmatter.tags:
        meta.append(MetaTag(property="article:tag", content=tag))

    return meta
