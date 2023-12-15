import datetime as dt
from pathlib import Path
from textwrap import dedent
from typing import Optional

import pytest

from server.di import resolve
from server.domain.entities import ImageObject, Keyword
from server.domain.repositories import CategoryRepository, KeywordRepository
from server.infrastructure.content import build_blog_posting
from server.infrastructure.html import build_meta_tags


@pytest.mark.asyncio
@pytest.mark.usefixtures("isolated_db")
async def test_build_blog_posting() -> None:
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
    image = "/static/img/articles/example.jpg"

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
        image: "{image}"
        ---
        You should *really* care about readability.
        """
    )

    blog_posting = await build_blog_posting(root, path, raw)

    essays = await category_repository.find_by_slug("essays")
    assert essays is not None

    python = await keyword_repository.find_by_name("python")
    assert python is not None

    assert blog_posting.name == title
    assert blog_posting.abstract == description
    assert blog_posting.text == (
        "<p>You should <em>really</em> care about readability.</p>"
    )
    assert blog_posting.slug == "readability-counts"
    assert blog_posting.edit_url == (
        "https://github.com/florimondmanca/www/blob/master/content/en/posts/2020/01/readability-counts.md"  # noqa: E501
    )
    assert blog_posting.date_published == dt.date(2020, 1, 1)
    assert blog_posting.category == essays
    assert blog_posting.in_language == "en"
    assert blog_posting.image == ImageObject(content_url=image, caption=None)
    assert blog_posting.thumbnail_url == image
    assert blog_posting.keywords == [Keyword(name="python", in_language="en")]

    meta = build_meta_tags(blog_posting)
    url = "https://florimond.dev/en/posts/2020/01/readability-counts"
    assert {"property": "og:title", "content": f"{title} - Florimond Manca"} in meta
    assert {"property": "og:description", "content": description} in meta
    assert {"property": "og:url", "content": url} in meta
    assert {"property": "og:image", "content": f"https://florimond.dev{image}"} in meta
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
    "image, image_thumbnail_line, expected_thumbnail_url",
    [
        pytest.param(
            "/static/img.jpg",
            "",
            "/static/img.jpg",
            id="default:static-file",
        ),
        pytest.param(
            "/elsewhere/img.jpg",
            "",
            None,
            id="default:non-static-file",
        ),
        pytest.param(
            "https://example.org/img.jpg",
            "",
            None,
            id="default:remote-url",
        ),
        pytest.param(
            "/static/img.jpg",
            "image_thumbnail: __auto__",
            "/static/img_thumbnail.jpg",
            id="auto:static-file",
        ),
        pytest.param(
            "/elsewhere/img.jpg",
            "image_thumbnail: __auto__",
            None,
            id="auto:non-static-file",
        ),
        pytest.param(
            "https://example.org/img.jpg",
            "image_thumbnail: __auto__",
            None,
            id="auto:remote-url",
        ),
    ],
)
async def test_image_thumbnail(
    image: str, image_thumbnail_line: str, expected_thumbnail_url: Optional[str]
) -> None:
    root = Path("content")
    path = Path("content/en/posts/2020/01/test.md")
    raw = dedent(
        f"""
        ---
        title: "Test"
        description: "Test"
        date: "2020-01-01"
        category: essays
        image: "{image}"
        {image_thumbnail_line}
        ---
        """
    )
    blog_posting = await build_blog_posting(root, path, raw)
    assert blog_posting.thumbnail_url == expected_thumbnail_url


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
    blog_posting = await build_blog_posting(root, path, raw)
    assert blog_posting.is_private is is_private
