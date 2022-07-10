from pathlib import Path
from textwrap import dedent
from typing import Optional

import pytest

from server.domain.entities import Tag
from server.infrastructure.filesystem import ContentItem
from server.infrastructure.pages import build_pages


def test_build_pages_empty() -> None:
    pages = build_pages([])
    assert pages == []


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
            location=Path("en/posts/readability-counts.md"),
        )
    ]

    pages = build_pages(items)

    readability_counts, python, essays = pages

    assert readability_counts.permalink == "/en/posts/readability-counts"
    assert readability_counts.frontmatter.title == title
    assert readability_counts.frontmatter.description == description
    assert readability_counts.frontmatter.date == date
    assert readability_counts.frontmatter.category == category
    assert readability_counts.frontmatter.tags == [Tag("python")]
    assert readability_counts.frontmatter.image == image

    meta = readability_counts.meta
    url = "https://florimond.dev/en/posts/readability-counts/"
    assert {"name": "twitter:card", "content": "summary_large_image"} in meta
    assert {"name": "twitter:title", "content": title} in meta
    assert {"name": "twitter:description", "content": description} in meta
    assert {"name": "twitter:url", "content": url} in meta
    assert {"name": "twitter:image", "content": f"https://florimond.dev{image}"} in meta
    assert {"property": "article:tag", "content": "python"} in meta

    assert readability_counts.html == (
        "<p>You should <em>really</em> care about readability.</p>"
    )

    assert python.permalink == "/en/tag/python"
    assert python.frontmatter.title
    assert python.frontmatter.description
    assert python.frontmatter.date is None
    assert python.frontmatter.tags == []
    assert python.frontmatter.tag == Tag("python")

    meta = python.meta
    url = "https://florimond.dev/en/tag/python/"
    assert {"name": "twitter:card", "content": "summary_large_image"} in meta
    assert {"name": "twitter:title", "content": python.frontmatter.title} in meta
    assert {
        "name": "twitter:description",
        "content": python.frontmatter.description,
    } in meta
    assert {"name": "twitter:url", "content": url} in meta

    assert essays.permalink == "/en/category/essays"
    assert "Essays" in essays.frontmatter.title
    assert essays.frontmatter.description
    assert essays.frontmatter.date is None
    assert essays.frontmatter.category == category
    assert essays.frontmatter.tags == []

    meta = essays.meta
    url = "https://florimond.dev/en/category/essays/"
    assert {"name": "twitter:card", "content": "summary_large_image"} in meta
    assert {"name": "twitter:title", "content": essays.frontmatter.title} in meta
    assert {
        "name": "twitter:description",
        "content": essays.frontmatter.description,
    } in meta
    assert {"name": "twitter:url", "content": url} in meta


@pytest.mark.parametrize(
    "image, image_thumbnail_line, expected_image_thumbnail",
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
def test_image_thumbnail(
    image: str, image_thumbnail_line: str, expected_image_thumbnail: Optional[str]
) -> None:
    item = ContentItem(
        content=dedent(
            f"""
            ---
            title: "Test"
            description: "Test"
            date: "2020-01-01"
            image: "{image}"
            {image_thumbnail_line}
            ---
            """
        ),
        location=Path("en/posts/test.md"),
    )

    (page,) = build_pages([item])
    assert page.frontmatter.image_thumbnail == expected_image_thumbnail


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
            location=Path(location),
        ),
    ]

    (page,) = build_pages(items)

    assert page.is_private is is_private
