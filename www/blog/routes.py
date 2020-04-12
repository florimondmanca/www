import datetime as dt
import typing

from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Route, WebSocketRoute

from .. import resources, settings
from .reload import hotreload
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


routes: typing.List[BaseRoute] = [
    Route("/", endpoint=RenderPage, name="home"),
    Route("/{permalink:path}/", endpoint=RenderPage, name="page"),
]

if settings.DEBUG:
    routes += [WebSocketRoute("/hot-reload", hotreload, name="hot-reload")]
