import glob
import pathlib
import typing

import aiofiles
import frontmatter as fm
import markdown

from .models import Frontmatter, Index, Page


async def load_index(index: Index) -> None:
    index.clear()
    await _load_pages(index)
    _generate_tag_pages(index)


def is_article(page: Page) -> bool:
    return page.permalink.startswith("/articles")


def get_articles(index: Index) -> typing.Iterator[Page]:
    return index.find_all(is_article)


async def _load_pages(index: Index) -> None:
    for path in _discover_page_paths(index.root):
        async with aiofiles.open(path) as f:
            page_content = await f.read()
        html, frontmatter = _compile_page(page_content)
        permalink = _permalink_from_path(path.relative_to(index.root))
        page = Page(html=html, permalink=permalink, frontmatter=frontmatter)
        index.insert(page)


def _get_unique_tags(index: Index) -> typing.Set[str]:
    return {tag for page in get_articles(index) for tag in page.frontmatter.tags}


def _generate_tag_pages(index: Index) -> None:
    for tag in _get_unique_tags(index):
        permalink = f"/tag/{tag}"
        frontmatter = Frontmatter(
            title=f"{tag.capitalize()} - Florimond Manca",
            description=f"Articles about #{tag}",
            tag=tag,
        )
        page = Page(permalink=permalink, frontmatter=frontmatter)
        index.insert(page)


def _compile_page(content: str) -> typing.Tuple[str, Frontmatter]:
    post = fm.loads(content)

    html = _compile_markdown(post.content)

    frontmatter = Frontmatter(
        home=post.get("home", False),
        title=post["title"],
        description=post["description"],
        date=post.get("date", ""),
        image=post.get("image"),
        image_caption=post.get("image_caption"),
        tags=post.get("tags", []),
    )

    return html, frontmatter


def _compile_markdown(content: str) -> str:
    return markdown.markdown(content, extensions=["codehilite", "fenced_code"])


def _discover_page_paths(root: pathlib.Path) -> typing.Iterator[pathlib.Path]:
    pattern = str(root / "**" / "*.md")
    for path in glob.glob(pattern, recursive=True):
        yield pathlib.Path(path)


def _permalink_from_path(path: pathlib.Path) -> str:
    url, _, extension = str(path).partition(".")
    assert extension == "md"

    segments = url.split("/")
    assert segments

    if segments[-1] == "README":
        segments[-1] = ""

    return "/" + "/".join(segments)
