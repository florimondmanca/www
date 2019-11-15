from starlette.staticfiles import StaticFiles
from starlette.types import Receive, Scope, Send

from . import settings
from .middleware import Raise404Middleware

static = Raise404Middleware(StaticFiles(directory=str(settings.BUILD_DIR)))


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    if is_page(scope["path"]):
        # Be sure to append 'index.html' as VuePress outputs pages
        # into folders containing a single 'index.html' file.
        scope["path"] = ensure_ends_with_index_html(scope["path"])

    await static(scope, receive, send)


def is_page(path: str) -> bool:
    return not path.startswith(("/assets", "/fonts", "/img"))


def ensure_ends_with_index_html(path: str) -> str:
    path = path.rstrip("/")
    if not path.endswith("/index.html"):
        return f"{path}/index.html"
    return path
