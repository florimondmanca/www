import markdown as md

from . import settings
from .domain.repositories import PageRepository

page_repository = PageRepository()

markdown = md.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
