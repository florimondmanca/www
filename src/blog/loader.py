import glob
import pathlib
import typing

import aiofiles
import frontmatter as fm

from .models import Frontmatter, MetaTag, Page
from .resources import markdown


async def load_pages(root: pathlib.Path) -> typing.List[Page]:
    pages = []

    async for page in _find_filesystem_pages(root):
        pages.append(page)

    unique_tags = {tag for page in pages for tag in page.frontmatter.tags}

    for page in _generate_tag_pages(unique_tags):
        pages.append(page)

    return pages


async def _find_filesystem_pages(root: pathlib.Path) -> typing.AsyncIterator[Page]:
    for path in _find_markdown_files(root):
        async with aiofiles.open(path) as f:
            content = await f.read()

        post = fm.loads(content)
        html = markdown.reset().convert(post.content)
        permalink = _permalink_from_path(path.relative_to(root))
        frontmatter = Frontmatter(
            home=post.get("home", False),
            title=post["title"],
            description=post.get("description"),
            date=post.get("date"),
            image=post.get("image"),
            image_caption=post.get("image_caption"),
            tags=post.get("tags", []),
        )
        meta = _build_meta(permalink, frontmatter)

        yield Page(html=html, permalink=permalink, frontmatter=frontmatter, meta=meta)


def _find_markdown_files(root: pathlib.Path) -> typing.Iterator[pathlib.Path]:
    pattern = str(root / "**" / "*.md")
    for path in glob.glob(pattern, recursive=True):
        yield pathlib.Path(path)


def _generate_tag_pages(tags: typing.Iterable[str]) -> typing.Iterator[Page]:
    for tag in tags:
        frontmatter = Frontmatter(
            title=f"{tag.capitalize()} - Florimond Manca",
            description=f"Articles about #{tag}",
            tag=tag,
        )
        permalink = f"/tag/{tag}"
        meta = _build_meta(permalink, frontmatter)

        yield Page(permalink=permalink, frontmatter=frontmatter, meta=meta)


def _permalink_from_path(path: pathlib.Path) -> str:
    url, _, extension = str(path).partition(".")
    assert extension == "md"

    segments = url.split("/")
    assert segments

    if segments[-1] == "README":
        segments[-1] = ""

    return "/" + "/".join(segments)


def _build_meta(permalink: str, frontmatter: Frontmatter) -> typing.List["MetaTag"]:
    url = f"https://florimond.dev/blog{permalink}"

    meta = [
        # General
        MetaTag(name="description", content=frontmatter.description),
        MetaTag(name="image", content=frontmatter.image),
        MetaTag(itemprop="name", content=frontmatter.title),
        MetaTag(itemprop="description", content=frontmatter.description),
        MetaTag(itemprop="image", content=frontmatter.image),
        # Twitter
        MetaTag(name="twitter:url", content=url),
        MetaTag(name="twitter:title", content=frontmatter.title),
        MetaTag(name="twitter:description", content=frontmatter.description),
        MetaTag(name="twitter:image", content=frontmatter.image),
        MetaTag(name="twitter:card", content="summary_large_image"),
        MetaTag(name="twitter:site", content="@florimondmanca"),
        # OpenGraph
        MetaTag(name="og:url", content=url),
        MetaTag(property="og:type", content="article"),
        MetaTag(property="og:title", content=frontmatter.title),
        MetaTag(property="og:description", content=frontmatter.description),
        MetaTag(property="og:image", content=frontmatter.image),
        MetaTag(property="og:site_name", content="Florimond Manca"),
        MetaTag(property="article:published_time", content=frontmatter.date),
    ]

    for tag in frontmatter.tags:
        meta.append(MetaTag(property="article:tag", content=tag))

    return meta
