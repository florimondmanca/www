from ddtrace_asgi.middleware import TraceMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.routing import Host, Mount, Route

from . import blog, caching, middleware, monitoring, resources, settings
from .endpoints import DomainRedirect


async def home(request: Request) -> Response:
    return resources.templates.TemplateResponse(
        "index.html.jinja", context={"request": request}
    )


async def error(request: Request) -> Response:
    if settings.TESTING:
        raise RuntimeError("Example server error")
    return RedirectResponse("/")  # pragma: no cover


async def not_found(request: Request, exc: Exception) -> Response:
    return resources.templates.TemplateResponse(
        "404.html.jinja", context={"request": request}, status_code=404
    )


async def internal_server_error(request: Request, exc: Exception) -> Response:
    return resources.templates.TemplateResponse(
        "500.html.jinja", context={"request": request}, status_code=500
    )


app = Starlette(
    debug=settings.DEBUG,
    routes=[
        Host("florimondmanca.com", app=DomainRedirect("florimond.dev")),
        Host(
            "blog.florimondmanca.com",
            app=DomainRedirect("blog.florimond.dev"),
            name="legacy__blog_dot_com",
        ),
        Host(
            "blog.florimond.dev",
            app=DomainRedirect("florimond.dev", root_path="/blog"),
            name="legacy__blog_dot_dev",
        ),
        Route("/", home),
        Route("/error", error),
        Mount("/blog", routes=blog.routes, name="blog"),
        Mount(settings.STATIC_ROOT, resources.static, name="static"),
        # Make the SCSS source available to browsers for inspection.
        Mount("/sass", resources.sass),
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
    ],
    middleware=[
        # NOTE: order matters (middleware executes from top to bottom).
        Middleware(
            middleware.ContextMiddleware, request_contextvar=resources.CTX_VAR_REQUEST
        ),
        Middleware(
            monitoring.MetricsMiddleware,
            known_domains=settings.KNOWN_DOMAINS,
            statsd=resources.statsd,
        ),
        Middleware(
            middleware.LegacyRedirectMiddleware,
            url_mapping=settings.BLOG_LEGACY_URL_MAPPING,
            root_path="/blog",
        ),
        Middleware(
            TraceMiddleware,
            service="www",
            tracer=resources.tracer,
            tags=", ".join(settings.DD_TAGS),
        ),
        Middleware(caching.CacheMiddleware, patterns=["/static/fonts/*"], ttl=3600),
    ],
    exception_handlers={404: not_found, 500: internal_server_error},
    on_startup=[monitoring.on_startup, *blog.on_startup],
    on_shutdown=[*blog.on_shutdown],
)
