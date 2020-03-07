import functools
import typing

import datadog
from ddtrace import Span
from ddtrace.ext import http
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from .utils import is_static_asset


class MetricsMiddleware:
    def __init__(self, app: ASGIApp, known_domains: typing.Sequence[str]) -> None:
        self.app = app
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
        if scope["type"] != "http" or is_static_asset(scope["path"]):
            await self.app(scope, receive, send)
            return

        domain = self._get_domain(scope)
        send = functools.partial(self._send_with_metrics, domain, send)

        await self.app(scope, receive, send)


class FilterRedirectResponses:
    def process_trace(
        self, trace: typing.Sequence[Span]
    ) -> typing.Optional[typing.Sequence[Span]]:
        for span in trace:
            if span.parent_id is not None or span.get_tag(http.STATUS_CODE) is None:
                continue

            try:
                status_code = int(span.get_tag(http.STATUS_CODE))
            except ValueError:
                continue
            else:
                if 300 <= status_code < 400:
                    return None

        return trace


class FilterDropIf:
    def __init__(self, condition: typing.Callable[[], bool]) -> None:
        self.condition = condition

    def process_trace(self, trace: list) -> typing.Optional[list]:
        return None if self.condition() else trace