from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route, Router
from starlette.types import ASGIApp

from ..di import resolve
from .reload import HotReload
from .templating import Templates


def make_site_app(name: str, static: ASGIApp) -> ASGIApp:
    hotreload = resolve(HotReload)

    async def default(request: Request) -> Response:
        await request.send_push_promise("/static/css/diypedals/index.css")
        await request.send_push_promise("/static/css/diypedals/reset.css")

        templates = resolve(Templates)
        page = "index.jinja"
        context = {"request": request}
        return templates.TemplateResponse(f"sites/{name}/{page}", context)

    routes = [
        Mount("/static", static, name="static"),
        *hotreload.routes(),
        Route("/{path:path}", default),
    ]

    return Router(routes=routes)
