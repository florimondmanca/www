import datetime as dt
import typing

import ddtrace
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Route

from ..resources import CTX_VAR_REQUEST, templates, tracer
from .resources import index


class RenderPage(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        CTX_VAR_REQUEST.set(request)

        permalink = "/" + request.path_params.get("permalink", "")

        for page in index.pages:
            if page.permalink == permalink:
                break
        else:
            raise HTTPException(404)

        if page.is_article:
            span: ddtrace.Span = tracer.current_span()
            span.set_tag("article.permalink", page.permalink)

        context = {
            "request": request,
            "now": dt.datetime.utcnow(),
            "page": page,
            "get_articles": index.articles_by_date,
        }

        return templates.TemplateResponse("blog/main.jinja", context=context)


routes: typing.List[BaseRoute] = [
    Route("/", endpoint=RenderPage),
    Route("/{permalink:path}/", endpoint=RenderPage),
]
