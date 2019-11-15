import typing

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Mount, Route
from starlette.staticfiles import StaticFiles

from .. import blog, feature_flags
from . import settings
from .middleware import LegacyBlogRedirectMiddleware
from .resources import templates


async def home(request: Request) -> Response:
    return templates.TemplateResponse("index.html.jinja", context={"request": request})


static_files = StaticFiles(directory=str(settings.DIR / "static"))


routes: typing.List[BaseRoute] = [
    Route("/", home),
    *(
        [Mount("/blog", app=blog.app, name="blog")]
        if feature_flags.BLOG_ENABLED
        else []
    ),
    Mount("/static", static_files, name="static"),
    # These files need to be exposed at the root, not '/static/'.
    Route("/service-worker.js", static_files, name="service-worker"),
    Route("/robots.txt", static_files, name="robots"),
]

middleware: typing.List[Middleware] = [Middleware(LegacyBlogRedirectMiddleware)]


async def not_found(request: Request, exc: Exception) -> Response:
    return templates.TemplateResponse(
        "404.html.jinja", context={"request": request}, status_code=404
    )


async def internal_server_error(request: Request, exc: Exception) -> Response:
    return templates.TemplateResponse(
        "500.html.jinja", context={"request": request}, status_code=500
    )


async def show_feature_flags() -> None:
    print(f"BLOG_ENABLED = {feature_flags.BLOG_ENABLED}")


app = Starlette(
    debug=settings.DEBUG,
    routes=routes,
    middleware=middleware,  # type: ignore
    exception_handlers={404: not_found, 500: internal_server_error},
    on_startup=[show_feature_flags],
)
