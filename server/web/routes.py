from starlette.routing import BaseRoute, Host, Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles

from .. import settings
from ..di import resolve
from . import legacy, middleware, views
from .i18n.routing import LocaleRoute
from .reload import HotReload
from .sitemap import sitemap


def get_routes() -> list[BaseRoute]:
    static = StaticFiles(directory=str(settings.STATIC_DIR))

    hotreload = resolve(HotReload)

    routes = [
        Host(
            "florimondmanca.com",
            app=legacy.DomainRedirect("florimond.dev"),
            name="legacy:dot_com",
        ),
        Host(
            "blog.florimondmanca.com",
            app=legacy.DomainRedirect("blog.florimond.dev"),
            name="legacy:blog_dot_com",
        ),
        Host(
            "blog.florimond.dev",
            app=legacy.DomainRedirect("florimond.dev", root_path="/blog"),
            name="legacy:blog_dot_dev",
        ),
        Route("/error/", views.error),
        Route("/blog/", views.legacy_blog_home, name="legacy:blog_home"),
        Mount(settings.STATIC_ROOT, static, name="static"),
        # These files need to be exposed at the root, not '/static/'.
        Route("/favicon.ico", static, name="favicon"),
        Route("/robots.txt", static, name="robots"),
        Route("/sitemap.xml", sitemap, name="sitemap"),
        Route(
            "/feed.rss",
            # Make sure clients always receive the correct MIME type for the RSS feed,
            # as the content type Starlette guesses may vary across operating systems.
            middleware.PatchHeadersMiddleware(
                static, headers={"content-type": "application/rss+xml"}
            ),
            name="feed-rss",
        ),
        LocaleRoute("/", views.home),
        Route("/{permalink:path}/", views.RenderPage, name="page"),
    ]

    if settings.DEBUG:  # pragma: no cover
        routes += [WebSocketRoute("/hot-reload", hotreload, name="hot-reload")]

    return routes
