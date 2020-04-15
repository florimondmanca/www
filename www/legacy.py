import typing

from starlette import status
from starlette.datastructures import URL
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send


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
