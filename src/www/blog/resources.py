import markdown as md

from .. import settings
from .models import Index

index = Index()
markdown = md.Markdown(extensions=settings.BLOG_MARKDOWN_EXTENSIONS)
