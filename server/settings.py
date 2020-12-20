import json
import pathlib

from starlette.config import Config

from .markdown import ImageFigcaptions

config = Config(".env")

HERE = pathlib.Path(__file__).parent

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING: bool = config("TESTING", cast=bool, default=False)

SITE_TITLE = "Florimond Manca"

KNOWN_DOMAINS = [
    "localhost",
    "florimondmanca.com",
    "blog.florimondmanca.com",
    "florimond.dev",
    "blog.florimond.dev",
]

STATIC_ROOT = "/static"
STATIC_DIR = HERE / "static"
TEMPLATES_DIR = HERE / "templates"

# Images take too much room on the Web. Let's limit ourselves
# to reasonable sizes only.
IMAGE_ALLOWED_MAX_SIZE_KB = 32

CONTENT_DIR = HERE.parent / "content"
with open(HERE / "assets" / "legacy-blog-url-mapping.json") as f:
    LEGACY_URL_MAPPING = json.loads(f.read())
MARKDOWN_EXTENSIONS = ["codehilite", "fenced_code", "tables", ImageFigcaptions()]

UNSPLASH_IMAGE_WIDTH = 550
UNSPLASH_IMAGE_QUALITY = 50
UNSPLASH_IMAGE_THUMBNAIL_WIDTH = 320
UNSPLASH_IMAGE_THUMBNAIL_QUALITY = 30

SOCIAL_LINKS = [
    {
        "href": "https://github.com/florimondmanca",
        "name": "GitHub",
        "title": "GitHub (@florimondmanca)",
    },
    {
        "href": "https://twitter.com/florimondmanca",
        "name": "Twitter",
        "title": "Twitter (@florimondmanca)",
    },
    {
        "href": "https://www.linkedin.com/in/florimondmanca",
        "name": "LinkedIn",
        "title": "LinkedIn (florimondmanca)",
    },
    {
        "href": "https://dev.to/florimondmanca",
        "name": "DEV",
        "title": "DEV (@florimondmanca)",
    },
]
