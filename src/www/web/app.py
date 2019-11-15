import typing

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Host, Mount, Route
from starlette.staticfiles import StaticFiles

from .. import blog, feature_flags
from . import settings
from .endpoints import DomainRedirect
from .resources import templates


async def home(request: Request) -> Response:
    return templates.TemplateResponse("index.html.jinja", context={"request": request})


static_files = StaticFiles(directory=str(settings.DIR / "static"))


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
    exception_handlers={404: not_found, 500: internal_server_error},
    on_startup=[show_feature_flags],
)
