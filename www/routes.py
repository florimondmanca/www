from starlette.routing import Host, Mount, Route, WebSocketRoute

from . import endpoints, legacy, middleware, resources, settings
from .reload import hotreload

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
    Route("/", endpoints.home),
    Route("/error/", endpoints.error),
    Route("/blog/", endpoints.legacy_blog_home, name="legacy:blog_home"),
    Route("/blog/{permalink:path}/", endpoints.RenderPage, name="page"),
    Mount(settings.STATIC_ROOT, resources.static, name="static"),
    # These files need to be exposed at the root, not '/static/'.
    Route("/favicon.ico", resources.static, name="favicon"),
    Route("/robots.txt", resources.static, name="robots"),
    Route("/sitemap.xml", resources.static, name="sitemap"),
    Route(
        "/feed.rss",
        # Make sure clients always receive the correct MIME type for the RSS feed,
        # as the content type Starlette guesses may vary across operating systems.
        middleware.PatchHeadersMiddleware(
            resources.static, headers={"content-type": "application/rss+xml"}
        ),
        name="feed-rss",
    ),
]

if settings.DEBUG:
    routes += [WebSocketRoute("/hot-reload", hotreload, name="hot-reload")]
