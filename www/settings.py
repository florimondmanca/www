import json
import pathlib

from starlette.config import Config

from .markdown_extensions import ImageFigcaptions

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)

WEB_ROOT = pathlib.Path(__file__).parent
WEB_ASSETS_ROOT = WEB_ROOT / "assets"

WEB_DD_TRACE_SERVICE = config("DD_TRACE_SERVICE", cast=str, default="")
WEB_DD_TRACE_TAGS = config("DD_TRACE_TAGS", cast=str, default="")

BLOG_ROOT = WEB_ROOT / "blog"
BLOG_CONTENT_ROOT = WEB_ROOT.parent / "content"

with open(WEB_ASSETS_ROOT / "legacy-blog-url-mapping.json") as f:
    BLOG_LEGACY_URL_MAPPING = json.loads(f.read())

BLOG_MARKDOWN_EXTENSIONS = ["codehilite", "fenced_code", "tables", ImageFigcaptions()]
