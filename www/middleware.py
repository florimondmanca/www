import functools
import typing

import datadog
import ddtrace
from ddtrace.constants import MANUAL_DROP_KEY
from ddtrace.http import store_request_headers, store_response_headers
from starlette import status
from starlette.datastructures import URL, CommaSeparatedStrings, Headers, MutableHeaders
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send


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


class MetricsMiddleware:
    def __init__(
        self, app: ASGIApp, known_domains: typing.Sequence[str], enabled: bool = True,
    ) -> None:
        self.app = app
        self.enabled = enabled
        self.known_domains = known_domains

    def _get_domain(self, scope: Scope) -> str:
        headers = Headers(scope=scope)
        host = headers.get("host", "")
        domain = host.split(":")[0]

        if domain not in self.known_domains:
            return "unknown"

        return domain

    async def _send_with_metrics(
        self, domain: str, send: Send, message: Message
    ) -> None:
        if message.get("type") == "http.response.start":
            tags = [f"domain:{domain}"]

            if "status" in message:
                status_code: int = message["status"]
                tags.append(f"status_code:{status_code}")

            datadog.statsd.increment("www.hits", 1, tags=tags)

        await send(message)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if (
            not self.enabled
            or scope["type"] != "http"
            or is_static_asset(scope["path"])
        ):
            await self.app(scope, receive, send)
            return

        domain = self._get_domain(scope)
        send = functools.partial(self._send_with_metrics, domain, send)

        await self.app(scope, receive, send)


class TracingMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        service: str,
        tracer: ddtrace.Tracer,
        tags: str = "",
        enabled: bool = True,
    ) -> None:
        self.app = app
        self.enabled = enabled
        self.service = service
        self.tracer = tracer
        self.trace_config = ddtrace.settings.config.asgi
        self.tags = [tag.split(":") for tag in CommaSeparatedStrings(tags)]

    async def _send_with_tracing(self, send: Send, message: Message) -> None:
        span = self.tracer.current_span()

        if span is not None and message.get("type") == "http.response.start":
            if "status" in message:
                status_code: int = message["status"]
                span.set_tag("http.status_code", str(status_code))

                if 300 <= status_code < 400:
                    # Ignore traces for redirect responses.
                    span.set_tag(MANUAL_DROP_KEY)

            if "headers" in message:
                response_headers = Headers(raw=message["headers"])
                store_response_headers(
                    response_headers, span, self.trace_config,
                )

        await send(message)

    def _should_skip_tracing(self, request: Request) -> bool:
        if is_static_asset(request.url.path):
            return True
        return False

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if (
            not self.enabled
            or scope["type"] != "http"
            or is_static_asset(scope["path"])
        ):
            await self.app(scope, receive, send)
            return

        with self.tracer.trace(
            "asgi.request", service=self.service, span_type="http"
        ) as span:
            request = Request(scope=scope)
            headers = request.headers
            method = request.method.upper()
            url = request.url
            del request

            store_request_headers(headers, span, self.trace_config)
            span.resource = f"{method} {url.path}"
            span.set_tag("http.method", method)
            span.set_tag("url", str(url))

            for name, value in self.tags:
                span.set_tag(name, value)

            send = functools.partial(self._send_with_tracing, send)

            try:
                await self.app(scope, receive, send)
            except BaseException:
                span.set_traceback()
                raise


def is_static_asset(path: str) -> bool:
    if path.startswith("/static/"):
        return True

    _, _, suffix = path.rpartition("/")
    _, has_extension, _ = suffix.partition(".")
    if has_extension:
        return True

    return False
