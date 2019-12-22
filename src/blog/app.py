from starlette.routing import Mount, Route, Router
from starlette.types import ASGIApp

from . import views
from .middleware import LegacyBlogRedirectMiddleware, TemplatesEnvironmentMiddleware
from .resources import static

routes = [
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

app: ASGIApp = Router(routes=routes)
app = TemplatesEnvironmentMiddleware(app)
app = LegacyBlogRedirectMiddleware(app)
