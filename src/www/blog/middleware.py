from starlette.datastructures import MutableHeaders
from starlette.exceptions import HTTPException
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class Raise404Middleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def _send(message: Message) -> None:
            if message["type"] == "http.response.start" and message["status"] == 404:
                raise HTTPException(404, detail="Not found")
            await send(message)

        await self.app(scope, receive, _send)


class PatchHeaders:
    def __init__(self, app: ASGIApp, headers: dict) -> None:
        self.app = app
        self.headers = headers

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def _send(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(raw=message["headers"])
                headers.update(self.headers)
            await send(message)

        await self.app(scope, receive, _send)
