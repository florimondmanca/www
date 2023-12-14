from server.infrastructure.markdown import MarkdownParser


def test_image_figcaption() -> None:
    text, attrs = MarkdownParser().convert(
        "![A beautiful mind](https://example.com/a-beautiful-mind)"
    )

    assert text == (
        '<p><figure class="f-image">'
        '<img alt="A beautiful mind" src="https://example.com/a-beautiful-mind" />'
        "<figcaption>A beautiful mind</figcaption>"
        "</figure></p>"
    )

    assert not attrs
