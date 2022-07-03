import markdown as md

from . import settings

markdown = md.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
