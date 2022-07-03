import markdown as md

from server import settings
from server.application.markdown import MarkdownRenderer


class MarkdownRendererAdapter(MarkdownRenderer):
    def __init__(self) -> None:
        self._impl = md.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)

    def render(self, source: str) -> str:
        return self._impl.reset().convert(source)
