from starlette import status
from starlette.datastructures import URL
from starlette.responses import RedirectResponse
from starlette.routing import Mount, Route, Router
from starlette.types import ASGIApp, Receive, Scope, Send

from . import settings, views
from .resources import static

router = Router(
    routes=[
        Route("/", views.home, name="home"),
        Route(
            "/articles/{year:int}/{month:int}/{slug}",
            views.article_detail,
            name="article_detail",
        ),
        Route("/tag/{tag}", views.tag_detail, name="tag_detail"),
        Route("/feed.rss", static, name="feed-rss"),
        Mount("/static", static, name="static"),
    ]
)


def get_responder(scope: Scope) -> ASGIApp:
    if scope["path"] in settings.BLOG_LEGACY_URL_MAPPING:
        mapped_path = settings.BLOG_LEGACY_URL_MAPPING[scope["path"]]
        redirect_path = scope.get("root_path", "") + mapped_path
        response = RedirectResponse(
            URL(scope=scope).replace(path=redirect_path),
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
        )
        return response

    return router


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    responder = get_responder(scope)
    await responder(scope, receive, send)
