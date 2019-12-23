from starlette import status
from starlette.datastructures import URL, MutableHeaders
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from . import settings


class LegacyBlogRedirectMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["path"] in settings.BLOG_LEGACY_URL_MAPPING:
            mapped_path = settings.BLOG_LEGACY_URL_MAPPING[scope["path"]]
            redirect_path = scope.get("root_path", "") + mapped_path
            response = RedirectResponse(
                URL(scope=scope).replace(path=redirect_path),
                status_code=status.HTTP_301_MOVED_PERMANENTLY,
            )
            await response(scope, receive, send)
        else:
            await self.app(scope, receive, send)


class PatchHeadersMiddleware:
    def __init__(self, app: ASGIApp, path: str, headers: dict) -> None:
        self.app = app
        self.path = path
        self.headers = headers

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["path"] != self.path:
            await self.app(scope, receive, send)
            return

        async def _send(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(raw=message["headers"])
                headers.update(self.headers)
            await send(message)

        await self.app(scope, receive, _send)
