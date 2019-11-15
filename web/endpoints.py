from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.types import Receive, Scope, Send


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
        request = Request(scope)
        url = request.url.replace(hostname=self.domain)
        if self.root_path:
            url = url.replace(path=f"{self.root_path}{request.url.path}")
        response = RedirectResponse(url, status_code=self.status_code)
        await response(scope, receive, send)
