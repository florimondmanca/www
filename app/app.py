import typing

import jinja2
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings

app = Starlette(debug=settings.DEBUG)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@jinja2.contextfunction
def relative_url_for(context: dict, name: str, **path_params: typing.Any) -> str:
    request = context["request"]
    router = request.scope["router"]
    url_path = router.url_path_for(name, **path_params)
    return str(url_path)


templates.env.globals["relative_url_for"] = relative_url_for


@app.route("/", name="home")
async def dashboard(request):
    template = "index.html.jinja"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


@app.route("/500")
async def error(request):
    """An example error.
    
    Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request, exc):
    template = "404.html.jinja"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    template = "500.html.jinja"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)
