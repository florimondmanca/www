import datetime as dt
import typing

from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route, Router
from starlette.types import ASGIApp

from . import utils
from .middleware import LegacyBlogRedirectMiddleware
from .models import Page
from .resources import CTX_VAR_REQUEST, index, sass, static, templates


class RenderPage(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        CTX_VAR_REQUEST.set(request)

        permalink = request["path"]

        page = index.find_one(permalink=permalink)
        if page is None:
            raise HTTPException(404)

        context = {
            "request": request,
            "now": dt.datetime.utcnow(),
            "page": page,
            "get_articles": self.get_articles,
            "is_article": utils.is_article,
        }

        return templates.TemplateResponse("main.jinja", context=context)

    def get_articles(self) -> typing.Iterator[Page]:
        return reversed(
            sorted(utils.get_articles(index), key=lambda page: page.frontmatter.date)
        )


routes = [
    Route("/feed.rss", static, name="feed-rss"),
    Mount("/static", static),
    Mount("/sass", sass),
    Mount("/", app=RenderPage),
]

app: ASGIApp = Router(routes=routes)
app = LegacyBlogRedirectMiddleware(app)
