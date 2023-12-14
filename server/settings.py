import json
import pathlib

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

from .markdown import ImageFigcaptions

config = Config(".env")

HERE = pathlib.Path(__file__).parent

HOST: str = config("WWW_HOST", cast=str, default="localhost")
PORT: int = config("WWW_PORT", cast=int, default=8000)

DEBUG: bool = config("WWW_DEBUG", cast=bool, default=False)
TESTING: bool = config("WWW_TESTING", cast=bool, default=False)

SITE_TITLE = "Florimond Manca"

KNOWN_DOMAINS = [
    "localhost",
    "florimondmanca.com",
    "blog.florimondmanca.com",
    "florimond.dev",
    "blog.florimond.dev",
]

STATIC_ROOT = "/static"
STATIC_DIR = HERE / "web" / "static"
TEMPLATES_DIR = HERE / "web" / "templates"

LOCALE_DIR = HERE.parent / "locale"
LOCALE_DOMAIN = "messages"
LOCALE_TRANSLATIONS = ["fr_FR"]
LANGUAGES = ["en", "fr"]
LANGUAGE_LABELS = {
    "en": "EN",
    "fr": "FR",
}
DEFAULT_LANGUAGE = "en"

EXTRA_CONTENT_DIRS = [
    pathlib.Path(item)
    for item in config("WWW_EXTRA_CONTENT_DIRS", cast=CommaSeparatedStrings, default="")
]

# Images take too much room on the Web. Let's limit ourselves
# to reasonable sizes only.
IMAGE_ALLOWED_MAX_SIZE_KB = 32

CONTENT_DIR = HERE.parent / "content"
with open(HERE / "web" / "assets" / "legacy-blog-url-mapping.json") as f:
    LEGACY_URL_MAPPING = json.loads(f.read())
MARKDOWN_EXTENSIONS: list = [
    "codehilite",
    "fenced_code",
    "tables",
    "footnotes",
    "toc",
    ImageFigcaptions(),
]

SOCIAL_LINKS = [
    {
        "href": "https://github.com/florimondmanca",
        "name": "GitHub",
        "title": "GitHub (@florimondmanca)",
    },
    {
        "href": "https://fosstodon.org/@florimond",
        "name": "Mastodon",
        "title": "Mastodon (@florimond@fosstodon.org)",
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
