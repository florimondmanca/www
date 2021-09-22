import typing

from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from . import legacy, settings
from .i18n.middleware import LocaleMiddleware

middleware = [
    # NOTE: Middleware executes from top to bottom.
    Middleware(GZipMiddleware, minimum_size=1024),  # > 1kB only
    Middleware(
        legacy.LegacyRedirectMiddleware,
        url_mapping=settings.LEGACY_URL_MAPPING,
    ),
    Middleware(
        LocaleMiddleware,
        languages=settings.LANGUAGES,
        default_language=settings.DEFAULT_LANGUAGE,
    ),
]


class PatchHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, headers: dict) -> None:
        super().__init__(app)
        self.headers = headers

    async def dispatch(self, request: Request, call_next: typing.Callable) -> Response:
        response = await call_next(request)
        response.headers.update(self.headers)
        return response
