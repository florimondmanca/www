import datetime as dt

from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route

from .middleware import PatchHeadersMiddleware
from .resources import CTX_VAR_REQUEST, index, sass, static, templates


class RenderPage(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        CTX_VAR_REQUEST.set(request)

        permalink = request["path"]
        if permalink != "/":
            permalink = permalink.rstrip("/")

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

        return templates.TemplateResponse("main.jinja", context=context)


routes = [
    Route(
        "/feed.rss",
        # Make sure clients always receive the correct MIME type for the RSS feed,
        # as the content type Starlette guesses may vary across operating systems.
        PatchHeadersMiddleware(static, headers={"content-type": "application/rss+xml"}),
        name="feed-rss",
    ),
    Mount("/static", static),
    Mount("/sass", sass),
    Mount("/", app=RenderPage),
]
