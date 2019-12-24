import typing

from ddtrace_asgi.middleware import TraceMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.routing import BaseRoute, Host, Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import blog
from blog.middleware import LegacyRedirectMiddleware

from . import settings
from .endpoints import DomainRedirect

templates = Jinja2Templates(directory=str(settings.WEB_ROOT / "templates"))
static_files = StaticFiles(directory=str(settings.WEB_ROOT / "static"))


async def home(request: Request) -> Response:
    return templates.TemplateResponse("index.html.jinja", context={"request": request})


async def error(request: Request) -> Response:
    if settings.TESTING:
        raise RuntimeError("Example server error")
    return RedirectResponse("/")  # pragma: no cover


routes: typing.List[BaseRoute] = [
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
    Mount("/static", static_files, name="static"),
    # These files need to be exposed at the root, not '/static/'.
    Route("/favicon.ico", static_files, name="favicon"),
    Route("/service-worker.js", static_files, name="service-worker"),
    Route("/robots.txt", static_files, name="robots"),
    Route("/sitemap.xml", blog.static, name="sitemap"),
]

middleware: typing.List[typing.Optional[Middleware]] = [
    Middleware(
        TraceMiddleware,
        service=settings.WEB_DD_TRACE_SERVICE,
        tags=settings.WEB_DD_TRACE_TAGS,
    )
    if settings.WEB_DD_TRACE_SERVICE
    else None,
    Middleware(
        LegacyRedirectMiddleware,
        url_mapping=blog.settings.BLOG_LEGACY_URL_MAPPING,
        root_path="/blog",
    ),
]


async def not_found(request: Request, exc: Exception) -> Response:
    return templates.TemplateResponse(
        "404.html.jinja", context={"request": request}, status_code=404
    )


async def internal_server_error(request: Request, exc: Exception) -> Response:
    return templates.TemplateResponse(
        "500.html.jinja", context={"request": request}, status_code=500
    )


app = Starlette(
    debug=settings.DEBUG,
    middleware=middleware,
    routes=routes,
    exception_handlers={404: not_found, 500: internal_server_error},
    on_startup=[blog.on_startup],
)
