import typing

from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.routing import BaseRoute, Route, WebSocketRoute

from .. import resources, settings
from .reload import hotreload
from .resources import index


async def home(request: Request) -> Response:
    return RedirectResponse(request.url_for("home"))


class RenderPage(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        permalink = "/" + request.path_params["permalink"]

        for page in index.pages:
            if page.permalink == permalink:
                break
        else:
            raise HTTPException(404)

        context = {
            "request": request,
            "page": page,
            "get_articles": index.articles_by_date,
        }

        return resources.templates.TemplateResponse("views/page.jinja", context=context)


routes: typing.List[BaseRoute] = [
    Route("/", endpoint=home, name="home"),
    Route("/{permalink:path}/", endpoint=RenderPage, name="page"),
]

if settings.DEBUG:
    routes += [WebSocketRoute("/hot-reload", hotreload, name="hot-reload")]
