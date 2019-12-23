import typing

from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route, Router
from starlette.types import ASGIApp

from . import utils
from .exceptions import DoesNotExist
from .middleware import LegacyBlogRedirectMiddleware, TemplatesEnvironmentMiddleware
from .models import Page
from .resources import index, static, templates


class RenderPage(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        permalink = request["path"]

        try:
            page = index.find_one_or_error(permalink=permalink)
        except DoesNotExist:
            raise HTTPException(404)

        context = {
            "request": request,
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
    Mount("/", app=RenderPage),
]

app: ASGIApp = Router(routes=routes)
app = TemplatesEnvironmentMiddleware(app)
app = LegacyBlogRedirectMiddleware(app)
