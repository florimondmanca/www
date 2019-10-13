from starlette.applications import Starlette
from starlette.templating import Jinja2Templates

from . import settings

templates = Jinja2Templates(directory="templates")

app = Starlette(debug=settings.DEBUG)


@app.route("/", name="home")
async def dashboard(request):
    template = "index.jinja"
    context = {"request": request}
    return templates.TemplateResponse(template, context)
