import glob
from pathlib import Path
from typing import Any, AsyncIterator, Dict, Iterable, Iterator, List, Optional, Tuple

import aiofiles
import frontmatter as fm
from typing_extensions import TypeGuard

from . import settings
from .application.markdown import MarkdownRenderer
from .di import resolve
from .domain.entities import ContentItem, Frontmatter, Page
from .domain.repositories import PageRepository
from .i18n import gettext_lazy as _
from .i18n import using_locale
from .utils import to_production_url


async def load_content() -> None:
    page_repository = resolve(PageRepository)

    items = [item async for item in _load_content_items()]

    for language in settings.LANGUAGES:
        for page in build_pages(items, language=language):
            page_repository.save(page)


def iter_content_paths() -> Iterator[Tuple[Path, Path]]:
    content_dirs = [settings.CONTENT_DIR, *settings.EXTRA_CONTENT_DIRS]
    for root in content_dirs:
        pattern = str(root / "**" / "*.md")
        for path in glob.glob(pattern, recursive=True):
            yield root, Path(path)


async def _load_content_items() -> AsyncIterator[ContentItem]:
    for root, path in iter_content_paths():
        async with aiofiles.open(path) as f:
            content = await f.read()
            yield ContentItem(
                content=content,
                location=str(path.relative_to(root)),
            )


def build_pages(items: List[ContentItem], *, language: str) -> List[Page]:
    pages: List[Page] = []

    pages.extend(_build_content_pages(items))

    unique_tags = {tag for page in pages for tag in page.frontmatter.tags}
    pages.extend(_generate_tag_pages(unique_tags, language=language))

    unique_categories = sorted(
        {
            page.frontmatter.category
            for page in pages
            if page.frontmatter.category is not None
        },
        key=list(_CATEGORY_LABELS).index,
    )
    pages.extend(_generate_category_pages(unique_categories, language=language))

    return pages


def _build_content_pages(items: List[ContentItem]) -> Iterator[Page]:
    markdown = resolve(MarkdownRenderer)

    for item in items:
        post = fm.loads(item.content)
        content = post.content
        html = markdown.render(content)
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


def _is_self_hosted(image: Optional[str]) -> TypeGuard[str]:
    return isinstance(image, str) and image.startswith(settings.STATIC_ROOT)


def _process_image(post: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    image = post.get("image")
    image_thumbnail = post.get("image_thumbnail")

    if image_thumbnail is None and _is_self_hosted(image):
        # By default, use the same image
        image_thumbnail = image

    if image_thumbnail == "__auto__":
        # Convention: '/static/example.jpg' -> '/static/example_thumbnail.jpg'
        image_thumbnail = (
            _append_filename(image, "_thumbnail") if _is_self_hosted(image) else None
        )

    assert image is None or isinstance(image, str)
    assert image_thumbnail is None or isinstance(image_thumbnail, str)

    return image, image_thumbnail


def _append_filename(filename: str, suffix: str) -> str:
    path = Path(filename)
    name = f"{path.stem}{suffix}{path.suffix}"
    return str(path.with_name(name))


def _generate_tag_pages(tags: Iterable[str], *, language: str) -> Iterator[Page]:
    for tag in tags:
        frontmatter = Frontmatter(
            title=f"{tag.capitalize()} - {settings.SITE_TITLE}",
            description=f"Posts about #{tag}",
            tag=tag,
        )
        permalink = f"/{language}/tag/{tag}"
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


def _generate_category_pages(
    categories: Iterable[str], *, language: str
) -> Iterator[Page]:
    with using_locale(language):
        for category in categories:
            label = get_category_label(category)
            frontmatter = Frontmatter(
                title=f"{label} - {settings.SITE_TITLE}",
                description=label,
                category=category,
            )
            permalink = f"/{language}/category/{category}"
            meta = _build_meta(permalink, frontmatter)

            yield Page(permalink=permalink, frontmatter=frontmatter, meta=meta)


def _build_permalink(location: str) -> str:
    url, _, extension = location.partition(".")
    assert extension == "md"

    segments = url.split("/")
    assert segments

    return "/" + "/".join(segments)


def _build_meta(permalink: str, frontmatter: Frontmatter) -> List[dict]:
    path = permalink + ("" if permalink.endswith("/") else "/")
    url = f"https://florimond.dev{path}"

    image_url = frontmatter.image
    if image_url:
        image_url = to_production_url(image_url)

    meta: list[dict] = [
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
        meta.append(dict(property="article:tag", content=tag))

    return meta
