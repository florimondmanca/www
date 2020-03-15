import markdown as md

from .. import settings
from .content_files import FilesystemContentFiles
from .hot_reload import FilesystemFileChangeDetector
from .models import Index

index = Index()
markdown = md.Markdown(extensions=settings.BLOG_MARKDOWN_EXTENSIONS)
file_change_detector = FilesystemFileChangeDetector()
content_files = FilesystemContentFiles(settings.BLOG_CONTENT_DIR)
