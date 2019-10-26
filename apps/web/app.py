import typing

import tldextract
from starlette.types import Scope, Receive, Send, ASGIApp
from starlette.datastructures import Headers
from apps import blog
from apps import index

SUBDOMAIN_TO_APP: typing.Dict[str, ASGIApp] = {"": index.app, "blog": blog.app}


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    headers = Headers(scope=scope)
    host = headers["host"]
    subdomain = tldextract.extract(host).subdomain
    app = SUBDOMAIN_TO_APP[subdomain]
    await app(scope, receive, send)
