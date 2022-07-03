from server.application.markdown import MarkdownRenderer
from server.di import resolve


def test_image_figcaption() -> None:
    markdown = resolve(MarkdownRenderer)

    content = markdown.render(
        "![A beautiful mind](https://example.com/a-beautiful-mind)"
    )

    assert content == (
        '<p><div class="p-image">'
        '<img alt="A beautiful mind" src="https://example.com/a-beautiful-mind" />'
        "<figcaption>A beautiful mind</figcaption>"
        "</div></p>"
    )
