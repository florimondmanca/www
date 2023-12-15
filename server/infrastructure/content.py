import datetime as dt
import glob
from pathlib import Path
from typing import AsyncIterator

from starlette.concurrency import run_in_threadpool

from .. import settings
from ..di import resolve
from ..domain.entities import Category, Keyword, Post
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
        keywords=keywords,
    )
