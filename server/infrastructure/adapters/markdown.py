import markdown as md

from server import settings

_impl = md.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)


def render(source: str) -> str:
    return _impl.reset().convert(source)
