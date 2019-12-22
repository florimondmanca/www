import typing

from starlette import status
from starlette.datastructures import URL
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from . import settings
from .resources import templates


class TemplatesEnvironmentMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: typing.Callable) -> Response:
        templates.env.globals["request"] = request
        try:
            return await call_next(request)
        finally:
            del templates.env.globals["request"]


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
