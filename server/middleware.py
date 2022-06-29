import typing

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from . import legacy, settings
from .i18n.middleware import LocaleMiddleware
from .i18n.routing import select_locale_by_request

middleware = [
    # NOTE: Middleware executes from top to bottom.
    Middleware(GZipMiddleware),
    Middleware(
        legacy.LegacyRedirectMiddleware,
        url_mapping=settings.LEGACY_URL_MAPPING,
    ),
    Middleware(
        LocaleMiddleware,
        default_locale=settings.DEFAULT_LANGUAGE,
        locales_dirs=["locale"],
        locale_selector=select_locale_by_request,
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
