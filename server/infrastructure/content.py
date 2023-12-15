import datetime as dt
import glob
from pathlib import Path
from typing import Any, AsyncIterator

from starlette.concurrency import run_in_threadpool

from .. import settings
from ..di import resolve
from ..domain.entities import Category, ImageObject, Keyword, Post
from ..domain.repositories import CategoryRepository, KeywordRepository
from .markdown import MarkdownParser


async def aiter_post_paths() -> AsyncIterator[tuple[Path, Path]]:
    content_dirs = [settings.CONTENT_DIR, *settings.EXTRA_CONTENT_DIRS]

    for root in content_dirs:
        pattern = str(root / "**" / "*.md")
        globbed = await run_in_threadpool(lambda: glob.glob(pattern, recursive=True))

        for path in map(Path, globbed):
            yield root, path


async def build_post(root: Path, path: Path, raw: str) -> Post:
    markdown_parser = resolve(MarkdownParser)
    category_repository = resolve(CategoryRepository)
    keyword_repository = resolve(KeywordRepository)

    html, attrs = markdown_parser.convert(raw)

    name = attrs["title"]
    abstract = attrs["description"]
    text = html
    slug = path.with_suffix("").parts[-1]
    edit_url = (
        "https://github.com/florimondmanca/www/blob/master"
        f"/{path.relative_to(root.parent)}"
    )
    date_published = dt.date.fromisoformat(attrs["date"])
    in_language = path.relative_to(root).parts[0]
    image, thumbnail_url = _process_image(attrs)

    category_slug = attrs["category"]
    category = await category_repository.find_by_slug(
        category_slug, language=in_language
    )

    if category is None:
        category_name = category_repository.make_name(
            category_slug, language=in_language
        )
        category = Category(
            name=category_name, slug=category_slug, in_language=in_language
        )
        await category_repository.save(category)

    keywords = []

    for kw in attrs.get("tags", []):
        keyword = await keyword_repository.find_by_name(kw, language=in_language)
        if keyword is None:
            keyword = Keyword(name=kw, in_language=in_language)
            await keyword_repository.save(keyword)
        keywords.append(keyword)

    return Post(
        name=name,
        abstract=abstract,
        text=text,
        slug=slug,
        edit_url=edit_url,
        date_published=date_published,
        category=category,
        in_language=in_language,
        image=image,
        thumbnail_url=thumbnail_url,
        keywords=keywords,
    )


def _process_image(attrs: dict[str, Any]) -> tuple[ImageObject | None, str | None]:
    image_url = attrs.get("image")
    image_caption = attrs.get("image_caption")
    image_thumbnail = attrs.get("image_thumbnail")

    is_image_self_hosted = isinstance(image_url, str) and image_url.startswith(
        settings.STATIC_ROOT
    )

    if image_thumbnail is None and is_image_self_hosted:
        # By default, use the same image
        image_thumbnail = image_url

    if image_thumbnail == "__auto__":
        # Convention: '/static/example.jpg' -> '/static/example_thumbnail.jpg'
        if is_image_self_hosted:
            assert isinstance(image_url, str)
            image_thumbnail = _append_filename(image_url, "_thumbnail")
        else:
            image_thumbnail = None

    assert image_url is None or isinstance(image_url, str)
    assert image_thumbnail is None or isinstance(image_thumbnail, str)

    if image_url is None:
        return (None, image_thumbnail)

    image = ImageObject(content_url=image_url, caption=image_caption)
    return (image, image_thumbnail)


def _append_filename(filename: str, suffix: str) -> str:
    path = Path(filename)
    name = f"{path.stem}{suffix}{path.suffix}"
    return str(path.with_name(name))
