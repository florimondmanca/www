import datetime as dt
import typing

from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route, Router
from starlette.types import ASGIApp

from . import utils
from .middleware import LegacyBlogRedirectMiddleware, PatchHeadersMiddleware
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

    def get_articles(self, tag: str = None) -> typing.List[Page]:
        return sorted(
            utils.get_articles(index, tag=tag),
            key=lambda page: page.frontmatter.date,
            reverse=True,
        )


routes = [
    Route("/feed.rss", static, name="feed-rss"),
    Mount("/static", static),
    Mount("/sass", sass),
    Mount("/", app=RenderPage),
]

app: ASGIApp = Router(routes=routes)
app = LegacyBlogRedirectMiddleware(app)
app = PatchHeadersMiddleware(
    # Make sure clients always receive the correct MIME type for the RSS feed,
    # as the content type Starlette guesses may vary across operating systems.
    app,
    path="/feed.rss",
    headers={"content-type": "application/rss+xml"},
)
