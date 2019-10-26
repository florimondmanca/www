from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

from . import resources, settings

app = Starlette(debug=settings.DEBUG)

app.mount("/static", resources.static_files, name="static")
# Service worker script must be served from root path
# so that all cached assets are in its "scope".
app.add_route("/service-worker.js", resources.static_files)


@app.route("/", name="home")
async def dashboard(request: Request) -> Response:
    template = "index.html.jinja"
    context = {"request": request}
    return resources.templates.TemplateResponse(template, context)


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
    return resources.templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request: Request, exc: Exception) -> Response:
    template = "500.html.jinja"
    context = {"request": request}
    return resources.templates.TemplateResponse(template, context, status_code=500)
