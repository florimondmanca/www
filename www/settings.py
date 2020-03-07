import json
import pathlib
from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

from .markdown_extensions import ImageFigcaptions

config = Config(".env")

HERE = pathlib.Path(__file__).parent

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING: bool = config("TESTING", cast=bool, default=False)

KNOWN_DOMAINS = [
    "localhost",
    "florimondmanca.com",
    "blog.florimondmanca.com",
    "florimond.dev",
    "blog.florimond.dev",
]

STATIC_ROOT = "/static"
STATIC_DIR = HERE / "static"
SASS_DIR = HERE / "sass"
TEMPLATES_DIR = HERE / "templates"

BLOG_CONTENT_DIR = HERE.parent / "content"
with open(HERE / "assets" / "legacy-blog-url-mapping.json") as f:
    BLOG_LEGACY_URL_MAPPING = json.loads(f.read())
BLOG_MARKDOWN_EXTENSIONS = ["codehilite", "fenced_code", "tables", ImageFigcaptions()]

DD_AGENT_HOST: str = config("DD_AGENT_HOST", cast=str, default="localhost")
DD_TRACE_TAGS: List[str] = config(
    "DD_TRACE_TAGS",
    cast=lambda value: list(CommaSeparatedStrings(value)),
    default="env:unknown",
)
DD_TRACE_FILTER_URLS: List[str] = [
    # Example: https://florimond.dev/static/picture.png
    rf"^https?://[^/]+{STATIC_ROOT}",
    # Example: https://florimond.dev/feed.rss
    r"^https?://(?P<domain>[^/]+)/(?P<file>[^/]+\.\w+)",
]
