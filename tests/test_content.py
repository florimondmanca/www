import datetime as dt
from pathlib import Path
from textwrap import dedent

import pytest

from server.di import resolve
from server.domain.entities import Keyword
from server.domain.repositories import CategoryRepository, KeywordRepository
from server.infrastructure.content import build_post
from server.infrastructure.html import build_meta_tags


@pytest.mark.asyncio
@pytest.mark.usefixtures("isolated_db")
async def test_build_post() -> None:
    category_repository = resolve(CategoryRepository)
    keyword_repository = resolve(KeywordRepository)

    essays = await category_repository.find_by_slug("essays")
    assert essays is None

    python = await keyword_repository.find_by_name("python")
    assert python is None

    title = "Readability Counts"
    description = "How readability impacts software development."
    date = "2020-01-01"
    category = "essays"

    root = Path("content")
    path = Path("content/en/posts/2020/01/readability-counts.md")
    raw = dedent(
        f"""
        ---
        title: "{title}"
        description: "{description}"
        date: "{date}"
        category: {category}
        tags:
          - python
        ---
        You should *really* care about readability.
        """
    )

    post = await build_post(root, path, raw)

    essays = await category_repository.find_by_slug("essays")
    assert essays is not None

    python = await keyword_repository.find_by_name("python")
    assert python is not None

    assert post.name == title
    assert post.abstract == description
    assert post.text == ("<p>You should <em>really</em> care about readability.</p>")
    assert post.slug == "readability-counts"
    assert post.edit_url == (
        "https://github.com/florimondmanca/www/blob/master/content/en/posts/2020/01/readability-counts.md"  # noqa: E501
    )
    assert post.date_published == dt.date(2020, 1, 1)
    assert post.category == essays
    assert post.in_language == "en"
    assert post.keywords == [Keyword(name="python", in_language="en")]

    meta = build_meta_tags(post)
    url = "https://florimond.dev/en/posts/2020/01/readability-counts"
    assert {"property": "og:title", "content": f"{title} - Florimond Manca"} in meta
    assert {"property": "og:description", "content": description} in meta
    assert {"property": "og:url", "content": url} in meta
    assert {"property": "article:tag", "content": "python"} in meta

    assert python.name == "python"
    assert python.in_language == "en"
    assert python.meta_title == "python - Florimond Manca"
    assert python.meta_description == "Posts with tag 'python'"

    meta = build_meta_tags(python)
    url = "https://florimond.dev/en/tag/python"
    assert {"property": "og:title", "content": "python - Florimond Manca"} in meta
    assert {"property": "og:description", "content": "Posts with tag 'python'"} in meta
    assert {"property": "og:url", "content": url} in meta

    assert essays.name == "Essays"
    assert essays.slug == "essays"
    assert essays.in_language == "en"

    meta = build_meta_tags(essays)
    url = "https://florimond.dev/en/category/essays"
    assert {"property": "og:title", "content": "Essays - Florimond Manca"} in meta
    assert {
        "property": "og:description",
        "content": "Posts in category 'Essays'",
    } in meta
    assert {"property": "og:url", "content": url} in meta


@pytest.mark.asyncio
@pytest.mark.usefixtures("isolated_db")
@pytest.mark.parametrize(
    "location, is_private",
    [
        ("en/posts/test.md", False),
        ("en/posts/test-prv.md", False),
        ("en/posts/test-prv-1.md", True),
        ("en/posts/test-prv-3535.md", True),
    ],
)
async def test_is_private(location: str, is_private: bool) -> None:
    root = Path("content")
    path = Path("content", location)
    raw = dedent(
        """
        ---
        title: "Test"
        description: "Test"
        date: "2020-01-01"
        category: essays
        ---
        """
    )
    post = await build_post(root, path, raw)
    assert post.is_private is is_private
