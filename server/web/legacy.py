from typing import Callable, Dict

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send


class LegacyRedirectMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        *,
        url_mapping: Dict[str, str],
    ) -> None:
        super().__init__(app)
        self.url_mapping = url_mapping

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path

        if path not in self.url_mapping:
            response = await call_next(request)

            # User may have requested `/xyz/` when only `/xyz` is
            # in the URL mapping, resulting in a 404 false-positive.
            # Attempt mapping from `/xyz`.
            if response.status_code != 404 or not path.endswith("/"):
                return response

            path = path.rstrip("/")
            if path not in self.url_mapping:
                return response

        redirect_path = self.url_mapping[path]

        return RedirectResponse(
            request.url.replace(path=redirect_path),
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
        )


class DomainRedirect:
    def __init__(
        self,
        domain: str,
        status_code: int = status.HTTP_301_MOVED_PERMANENTLY,
        root_path: str = None,
    ) -> None:
        self.domain = domain
        self.status_code = status_code
        self.root_path = root_path

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        assert scope["type"] == "http"

        request = Request(scope)
        url = request.url.replace(hostname=self.domain)
        if self.root_path:
            url = url.replace(path=f"{self.root_path}{request.url.path}")

        response = RedirectResponse(url, status_code=self.status_code)
        await response(scope, receive, send)
