import pathlib

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

HERE = pathlib.Path(__file__).parent

HOST: str = config("WWW_HOST", cast=str, default="localhost")
PORT: int = config("WWW_PORT", cast=int, default=8000)

DEBUG: bool = config("WWW_DEBUG", cast=bool, default=False)
TESTING: bool = config("WWW_TESTING", cast=bool, default=False)

STATIC_ROOT = "/static"
STATIC_DIR = HERE / "web" / "static"
TEMPLATES_DIR = HERE / "web" / "templates"

WEBDAV_USERNAME = config("DIYPEDALS_WEBDAV_USERNAME", default=None)
WEBDAV_PASSWORD: Secret = config("DIYPEDALS_WEBDAV_PASSWORD", cast=Secret, default=None)

BUILD_REPORTS_WEBDAV_URL = config("DIYPEDALS_BUILD_REPORTS_WEBDAV_URL", default=None)
BUILD_REPORTS_IMG_CDIR = STATIC_DIR / "diypedals" / "img" / "build_reports"
BUILD_REPORTS_CACHE_DIR = HERE / "cache"
