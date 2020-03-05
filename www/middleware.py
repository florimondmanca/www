import typing

import ddtrace
from starlette import status
from starlette.datastructures import URL, Headers, MutableHeaders
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from .resources import tracer


class LegacyRedirectMiddleware:
    def __init__(
        self, app: ASGIApp, *, url_mapping: typing.Dict[str, str], root_path: str,
    ) -> None:
        self.app = app
        self.root_path = root_path
        self.url_mapping = url_mapping

    def get_responder(self, scope: Scope) -> ASGIApp:
        if scope["type"] != "http":
            return self.app

        if not scope["path"].startswith(self.root_path):
            return self.app

        path = scope["path"][len(self.root_path) :]

        if path not in self.url_mapping:
            return self.app

        mapped_path = self.url_mapping[path]
        redirect_path = self.root_path + mapped_path

        return RedirectResponse(
            URL(scope=scope).replace(path=redirect_path),
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        responder = self.get_responder(scope)
        await responder(scope, receive, send)


class PatchHeadersMiddleware:
    def __init__(self, app: ASGIApp, headers: dict) -> None:
        self.app = app
        self.headers = headers

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def _send(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(raw=message["headers"])
                headers.update(self.headers)
            await send(message)

        await self.app(scope, receive, _send)


class RequestedHostSpanTagMiddleware:
    """
    Add the 'Host' header as a 'request_host' tag to any current trace span.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        span: ddtrace.Span = tracer.current_root_span()
        assert span is not None

        headers = Headers(scope=scope)
        host: str = headers.get("host", "")
        span.set_tag("requested_host", host)

        await self.app(scope, receive, send)
