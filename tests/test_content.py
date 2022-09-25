from pathlib import Path
from textwrap import dedent
from typing import Optional

import pytest

from server.application.queries import GetPages
from server.di import resolve
from server.domain.entities import Tag
from server.infrastructure.html import build_meta_tags
from server.infrastructure.sources import ContentItem, ContentSource
from server.seedwork.domain.cqrs import MessageBus


class StringSource(ContentSource):
    def __init__(self, content: str) -> None:
        self._content = content

    async def get(self) -> str:
        return self._content


@pytest.mark.asyncio
async def test_get_pages_empty() -> None:
    bus = resolve(MessageBus)
    pages = await bus.execute(GetPages(items=[]))
    assert pages == []


@pytest.mark.asyncio
async def test_get_pages() -> None:
    title = "Readability Counts"
    description = "How readability impacts software development."
    date = "2000-01-01"
    category = "essays"
    image = "/static/img/articles/example.jpg"

    items = [
        ContentItem(
            source=StringSource(
                dedent(
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
            ),
            location=Path("en/posts/readability-counts.md"),
        )
    ]

    bus = resolve(MessageBus)
    pages = await bus.execute(GetPages(items))

    readability_counts, python, essays = pages

    assert readability_counts.permalink == "/en/posts/readability-counts"
    assert readability_counts.metadata.title == title
    assert readability_counts.metadata.description == description
    assert readability_counts.metadata.date == date
    assert readability_counts.metadata.category is not None
    assert readability_counts.metadata.category.name == category
    assert readability_counts.metadata.tags == [Tag("python")]
    assert readability_counts.metadata.image == image

    meta = build_meta_tags(readability_counts)
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
    assert python.metadata.title
    assert python.metadata.description
    assert python.metadata.date is None
    assert python.metadata.tags == []
    assert python.metadata.tag == Tag("python")

    meta = build_meta_tags(python)
    url = "https://florimond.dev/en/tag/python/"
    assert {"name": "twitter:card", "content": "summary_large_image"} in meta
    assert {"name": "twitter:title", "content": python.metadata.title} in meta
    assert {
        "name": "twitter:description",
        "content": python.metadata.description,
    } in meta
    assert {"name": "twitter:url", "content": url} in meta

    assert essays.permalink == "/en/category/essays"
    assert "Essays" in essays.metadata.title
    assert essays.metadata.description
    assert essays.metadata.date is None
    assert essays.metadata.category is not None
    assert essays.metadata.category.name == category
    assert essays.metadata.tags == []

    meta = build_meta_tags(essays)
    url = "https://florimond.dev/en/category/essays/"
    assert {"name": "twitter:card", "content": "summary_large_image"} in meta
    assert {"name": "twitter:title", "content": essays.metadata.title} in meta
    assert {
        "name": "twitter:description",
        "content": essays.metadata.description,
    } in meta
    assert {"name": "twitter:url", "content": url} in meta


@pytest.mark.asyncio
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
async def test_image_thumbnail(
    image: str, image_thumbnail_line: str, expected_image_thumbnail: Optional[str]
) -> None:
    item = ContentItem(
        source=StringSource(
            dedent(
                f"""
            ---
            title: "Test"
            description: "Test"
            date: "2020-01-01"
            image: "{image}"
            {image_thumbnail_line}
            ---
            """
            )
        ),
        location=Path("en/posts/test.md"),
    )

    bus = resolve(MessageBus)
    (page,) = await bus.execute(GetPages([item]))

    assert page.metadata.image_thumbnail == expected_image_thumbnail


@pytest.mark.asyncio
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
    item = ContentItem(
        source=StringSource(
            dedent(
                """
                ---
                title: "Test"
                description: "Test"
                date: "2020-01-01"
                ---
                """
            )
        ),
        location=Path(location),
    )

    bus = resolve(MessageBus)
    (page,) = await bus.execute(GetPages([item]))

    assert page.is_private is is_private
