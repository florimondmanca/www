import glob
import pathlib
import typing

import aiofiles
import frontmatter as fm

from .models import Article, Frontmatter, Index


def parse_markdown_content(content: str) -> typing.Tuple[str, Frontmatter]:
    post = fm.loads(content)

    content = post.content
    frontmatter = Frontmatter(
        title=post["title"],
        description=post["description"],
        date=post["date"],
        tags=post.get("tags", []),
    )

    return content, frontmatter


def get_article_paths(root: pathlib.Path) -> typing.Iterator[pathlib.Path]:
    pattern = str(root / "**" / "*.md")
    for path in glob.glob(pattern, recursive=True):
        yield pathlib.Path(path)


async def load_index(index: Index) -> None:
    for path in get_article_paths(index.root):
        async with aiofiles.open(path) as f:
            markdown_content = await f.read()

        content, frontmatter = parse_markdown_content(markdown_content)

        year, month, filename = str(path.relative_to(index.root)).split("/")
        slug, _, extension = filename.partition(".")
        assert extension == "md"
        permalink = f"/{year}/{month}/{slug}"

        article = Article(
            content=content, permalink=permalink, slug=slug, frontmatter=frontmatter
        )

        index.insert(article)
