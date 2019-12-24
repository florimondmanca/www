import json
import pathlib

from .markdown_extensions import ImageFigcaptions

BLOG_ROOT = pathlib.Path(__file__).parent
BLOG_CONTENT_ROOT = BLOG_ROOT / "content"
BLOG_ASSETS_ROOT = BLOG_ROOT / "assets"

with open(BLOG_ASSETS_ROOT / "legacy-blog-url-mapping.json") as f:
    BLOG_LEGACY_URL_MAPPING = json.loads(f.read())

BLOG_MARKDOWN_EXTENSIONS = ["codehilite", "fenced_code", "tables", ImageFigcaptions()]
BLOG_GA_ID = "UA-122676386-2"
