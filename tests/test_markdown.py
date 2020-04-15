from www.resources import markdown


def test_image_figcaption() -> None:
    content = markdown.convert(
        "![A beautiful mind](https://example.com/a-beautiful-mind)"
    )

    assert content == (
        '<p><div class="p-markdown-image">'
        '<img alt="A beautiful mind" src="https://example.com/a-beautiful-mind" />'
        "<figcaption>A beautiful mind</figcaption>"
        "</div></p>"
    )
