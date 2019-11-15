from starlette import status
from starlette.datastructures import URL
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from . import config


class Raise404Middleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def _send(message: Message) -> None:
            if message["type"] == "http.response.start" and message["status"] == 404:
                raise HTTPException(404, detail="Not found")
            await send(message)

        await self.app(scope, receive, _send)


# This app serves all static files output by VuePress: HTML pages, JS, CSS, etc.
static = Raise404Middleware(StaticFiles(directory=str(config.BUILD_DIR)))


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    path = scope["path"]
    if path in config.BLOG_LEGACY_URL_MAPPING:
        redirect_path = config.BLOG_LEGACY_URL_MAPPING[path]
        url = URL(scope=scope)
        response = RedirectResponse(
            url=url.replace(path=scope.get("root_path", "") + redirect_path),
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
        )
        await response(scope, receive, send)
        return

    # Be sure to append 'index.html' as VuePress outputs pages
    # into folders containing a single 'index.html' file.
    if not is_asset(scope["path"]):
        scope["path"] = ensure_ends_with_index_html(path)

    await static(scope, receive, send)


def is_asset(path: str) -> bool:
    return path.startswith(("/assets", "/static"))


def ensure_ends_with_index_html(path: str) -> str:
    path = path.rstrip("/")
    if not path.endswith("/index.html"):
        return f"{path}/index.html"
    return path
