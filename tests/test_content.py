from textwrap import dedent
from typing import Optional

import pytest

from server.content import build_pages
from server.models import ContentItem


def test_build_pages_empty() -> None:
    pages = build_pages([])
    assert pages == {"en": [], "fr": []}


def test_build_pages() -> None:
    title = "Readability Counts"
    description = "How readability impacts software development."
    date = "2000-01-01"
    category = "essays"
    image = "/static/img/articles/example.jpg"

    items = [
        ContentItem(
            content=dedent(
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
            ),
            location="en/posts/readability-counts.md",
        )
    ]

    pages = build_pages(items)
    assert set(pages) == {"en", "fr"}

    readability_counts, python, essays = pages["en"]

    assert readability_counts.permalink == "/en/posts/readability-counts"
    assert readability_counts.frontmatter.title == title
    assert readability_counts.frontmatter.description == description
    assert readability_counts.frontmatter.date == date
    assert readability_counts.frontmatter.category == category
    assert readability_counts.frontmatter.tags == ["python"]
    assert readability_counts.frontmatter.image == image

    meta = [str(tag) for tag in readability_counts.meta]
    url = "https://florimond.dev/en/posts/readability-counts/"
    assert '<meta name="twitter:card" content="summary_large_image">' in meta
    assert f'<meta name="twitter:title" content="{title}">' in meta
    assert f'<meta name="twitter:description" content="{description}">' in meta
    assert f'<meta name="twitter:url" content="{url}">' in meta
    assert f'<meta name="twitter:image" content="https://florimond.dev{image}">' in meta
    assert '<meta property="article:tag" content="python">' in meta

    assert readability_counts.html == (
        "<p>You should <em>really</em> care about readability.</p>"
    )

    assert python.permalink == "/en/tag/python"
    assert python.frontmatter.title
    assert python.frontmatter.description
    assert python.frontmatter.date is None
    assert python.frontmatter.tags == []
    assert python.frontmatter.tag == "python"

    meta = [str(tag) for tag in python.meta]
    url = "https://florimond.dev/en/tag/python/"
    assert '<meta name="twitter:card" content="summary_large_image">' in meta
    assert f'<meta name="twitter:title" content="{python.frontmatter.title}">' in meta
    assert (
        f'<meta name="twitter:description" content="{python.frontmatter.description}">'
    ) in meta
    assert f'<meta name="twitter:url" content="{url}">' in meta

    assert essays.permalink == "/en/category/essays"
    assert "Essays" in essays.frontmatter.title
    assert essays.frontmatter.description
    assert essays.frontmatter.date is None
    assert essays.frontmatter.category == category
    assert essays.frontmatter.tags == []

    meta = [str(tag) for tag in essays.meta]
    url = "https://florimond.dev/en/category/essays/"
    assert '<meta name="twitter:card" content="summary_large_image">' in meta
    assert f'<meta name="twitter:title" content="{essays.frontmatter.title}">' in meta
    assert (
        f'<meta name="twitter:description" content="{essays.frontmatter.description}">'
        in meta
    )
    assert f'<meta name="twitter:url" content="{url}">' in meta


@pytest.mark.parametrize(
    "image, image_thumbnail",
    [
        pytest.param("/static/img.jpg", "/static/img_thumbnail.jpg", id="static-file"),
        pytest.param("/elsewhere/img.jpg", None, id="non-static-file"),
        pytest.param("https://example.org/img.jpg", None, id="remote-url"),
    ],
)
def test_image_auto_thumbnail(image: str, image_thumbnail: Optional[str]) -> None:
    item = ContentItem(
        content=dedent(
            f"""
            ---
            title: "Test"
            description: "Test"
            date: "2020-01-01"
            image: "{image}"
            ---
            """
        ),
        location="en/posts/test.md",
    )

    (page,) = build_pages([item])["en"]
    assert page.frontmatter.image_thumbnail == image_thumbnail


@pytest.mark.parametrize(
    "location, is_private",
    [
        ("en/posts/test.md", False),
        ("en/posts/test-prv.md", False),
        ("en/posts/test-prv-1.md", True),
        ("en/posts/test-prv-3535.md", True),
    ],
)
def test_is_private(location: str, is_private: bool) -> None:
    items = [
        ContentItem(
            content=dedent(
                """
                ---
                title: "Test"
                description: "Test"
                date: "2020-01-01"
                ---
                """
            ),
            location=location,
        ),
    ]

    (page,) = build_pages(items)["en"]

    assert page.is_private is is_private
