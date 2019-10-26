import pathlib
import typing

import jinja2
from starlette.applications import Starlette
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

config = Config()

DIR = pathlib.Path(__file__).parent
DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)

app = Starlette(debug=DEBUG)

static_files = StaticFiles(directory=str(DIR / "static"))
app.mount("/static", static_files, name="static")

# Service worker script must be served from root path
# so that all cached assets are in its "scope".
app.add_route("/service-worker.js", static_files)

templates = Jinja2Templates(directory=str(DIR / "templates"))


@jinja2.contextfunction
def relative_url_for(context: dict, name: str, **path_params: typing.Any) -> str:
    url_path = app.router.url_path_for(name, **path_params)
    return str(url_path)


templates.env.globals["relative_url_for"] = relative_url_for


@app.route("/", name="home")
async def dashboard(request: Request) -> Response:
    template = "index.html.jinja"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


@app.route("/500")
async def error(request: Request) -> Response:
    """An example error.

    Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request: Request, exc: Exception) -> Response:
    template = "404.html.jinja"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request: Request, exc: Exception) -> Response:
    template = "500.html.jinja"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)
