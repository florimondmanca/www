from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings

app = Starlette(debug=settings.DEBUG)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.route("/", name="home")
async def dashboard(request):
    template = "index.html.jinja"
    context = {"request": request}
    return templates.TemplateResponse(template, context)
