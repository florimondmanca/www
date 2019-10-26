import typing

import tldextract
from starlette.datastructures import Headers, URL
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class SubdomainRedirectMiddleware:
    def __init__(self, app: ASGIApp, mapping: typing.Dict[str, str]) -> None:
        self.app = app
        self.mapping = mapping

    def get_app(self, scope: Scope) -> ASGIApp:
        headers = Headers(scope=scope)
        url = URL(scope=scope)
        host = headers["host"]
        extract = tldextract.extract(host)
        domain = extract.domain
        subdomain = extract.subdomain

        if subdomain not in self.mapping:
            return self.app

        path = self.mapping[subdomain]
        redirect_url = url.replace(path=f"{path}{url.path}", hostname=domain)
        return RedirectResponse(url=str(redirect_url))

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        app = self.get_app(scope=scope)
        await app(scope, receive, send)
