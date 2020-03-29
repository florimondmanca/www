import datetime as dt
import typing

from starlette.concurrency import run_until_first_complete
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Route, WebSocketRoute
from starlette.websockets import WebSocket

from .. import resources, settings
from .resources import index


class RenderPage(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        permalink = "/" + request.path_params.get("permalink", "")

        for page in index.pages:
            if page.permalink == permalink:
                break
        else:
            raise HTTPException(404)

        context = {
            "request": request,
            "now": dt.datetime.utcnow(),
            "page": page,
            "get_articles": index.articles_by_date,
        }

        return resources.templates.TemplateResponse("blog/main.jinja", context=context)


async def hot_reload(ws: WebSocket) -> None:
    await ws.accept()

    async def watch_client_disconnects() -> None:
        async for _ in ws.iter_text():
            pass

    async def watch_reloads() -> None:
        channel = settings.BLOG_RELOAD_CHANNEL
        async with resources.broadcast.subscribe(channel=channel) as subscriber:
            async for event in subscriber:
                await ws.send_text(event.message)

    await run_until_first_complete(
        (watch_client_disconnects, {}), (watch_reloads, {}),
    )


routes: typing.List[BaseRoute] = [
    Route("/", endpoint=RenderPage, name="home"),
    Route("/{permalink:path}/", endpoint=RenderPage, name="page"),
]

if settings.DEBUG:
    routes += [WebSocketRoute("/hot-reload", hot_reload, name="hot-reload")]
