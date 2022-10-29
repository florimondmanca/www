from typing import Any

import frontmatter
import markdown as md

from .. import settings


class MarkdownParser:
    def __init__(self) -> None:
        self._impl = md.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)

    def convert(self, raw: str) -> tuple[str, dict[str, Any]]:
        post = frontmatter.loads(raw)
        html = self._impl.reset().convert(post.content)
        attrs = dict(post)
        return html, attrs
