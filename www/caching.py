import typing
from fnmatch import fnmatch

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, patterns: typing.List[str], ttl: int) -> None:
        super().__init__(app)
        self.patterns = patterns
        self.ttl = ttl

    def get_cache_headers(self, request: Request) -> dict:
        for pattern in self.patterns:
            if fnmatch(request.url.path, pattern):
                return {"Cache-Control": f"max-age={self.ttl}"}
        return {}

    async def dispatch(self, request: Request, call_next: typing.Callable) -> Response:
        response = await call_next(request)
        cache_headers = self.get_cache_headers(request)
        response.headers.update(cache_headers)
        return response
