import typing

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from . import caching, legacy, settings

middleware = [
    # NOTE: Middleware executes from top to bottom.
    Middleware(
        legacy.LegacyRedirectMiddleware,
        url_mapping=settings.LEGACY_URL_MAPPING,
        root_path="/blog",
    ),
    Middleware(caching.CacheMiddleware, patterns=["/static/fonts/*"], ttl=3600),
]


class PatchHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, headers: dict) -> None:
        super().__init__(app)
        self.headers = headers

    async def dispatch(self, request: Request, call_next: typing.Callable) -> Response:
        response = await call_next(request)
        response.headers.update(self.headers)
        return response
