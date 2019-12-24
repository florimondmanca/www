import glob
import pathlib
import typing

import aiofiles
import frontmatter as fm

from .models import Frontmatter, Page
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
        frontmatter = Frontmatter(
            home=post.get("home", False),
            title=post["title"],
            description=post.get("description"),
            date=post.get("date"),
            image=post.get("image"),
            image_caption=post.get("image_caption"),
            tags=post.get("tags", []),
        )

        permalink = _permalink_from_path(path.relative_to(root))

        yield Page(html=html, permalink=permalink, frontmatter=frontmatter)


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

        yield Page(permalink=permalink, frontmatter=frontmatter)


def _permalink_from_path(path: pathlib.Path) -> str:
    url, _, extension = str(path).partition(".")
    assert extension == "md"

    segments = url.split("/")
    assert segments

    if segments[-1] == "README":
        segments[-1] = ""

    return "/" + "/".join(segments)
