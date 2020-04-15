from textwrap import dedent

from www.content import build_pages
from www.models import ContentItem


def test_build_pages_empty() -> None:
    pages = build_pages([])
    assert pages == []


def test_build_pages() -> None:
    title = "Readability Counts"
    description = "How readability impacts software development."
    date = "2000-01-01"

    items = [
        ContentItem(
            content=dedent(
                f"""
                ---
                published: false
                title: "{title}"
                description: "{description}"
                date: "{date}"
                tags:
                - python
                ---
                You should *really* care about readability.
                """
            ),
            location="posts/readability-counts.md",
        )
    ]

    pages = build_pages(items)

    assert len(pages) == 2
    readability_counts, python = pages

    assert readability_counts.permalink == "/posts/readability-counts"
    assert readability_counts.frontmatter.title == title
    assert readability_counts.frontmatter.description == description
    assert readability_counts.frontmatter.date == date
    assert readability_counts.frontmatter.tags == ["python"]
    assert not readability_counts.frontmatter.home

    meta = [str(tag) for tag in readability_counts.meta]
    url = "https://florimond.dev/blog/posts/readability-counts"
    assert '<meta name="twitter:card" content="summary_large_image">' in meta
    assert f'<meta name="twitter:title" content="{title}">' in meta
    assert f'<meta name="twitter:description" content="{description}">' in meta
    assert f'<meta name="twitter:url" content="{url}">' in meta
    assert '<meta property="article:tag" content="python">' in meta

    assert readability_counts.html == (
        "<p>You should <em>really</em> care about readability.</p>"
    )

    assert python.permalink == "/tag/python"
    assert python.frontmatter.title
    assert python.frontmatter.description
    assert python.frontmatter.date is None
    assert python.frontmatter.tags == []
    assert python.frontmatter.tag == "python"
    assert not python.frontmatter.home

    meta = [str(tag) for tag in python.meta]
    url = "https://florimond.dev/blog/tag/python"
    assert '<meta name="twitter:card" content="summary_large_image">' in meta
    assert f'<meta name="twitter:title" content="{python.frontmatter.title}">' in meta
    assert (
        f'<meta name="twitter:description" content="{python.frontmatter.description}">'
    ) in meta
    assert f'<meta name="twitter:url" content="{url}">' in meta
