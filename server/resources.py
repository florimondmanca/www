import datetime as dt

import markdown as md
from starlette.exceptions import HTTPException
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings
from .models import Index
from .reload import hotreload

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
static = StaticFiles(directory=str(settings.STATIC_DIR))


def raise_server_error(message: str) -> None:  # pragma: no cover
    raise HTTPException(500, detail=message)


def dateformat(value: str) -> str:
    datevalue = dt.datetime.strptime(value, "%Y-%m-%d")
    return datevalue.strftime("%b %d, %Y")


templates.env.globals["now"] = dt.datetime.now
templates.env.globals["raise"] = raise_server_error
templates.env.globals["settings"] = settings
templates.env.globals["hotreload"] = hotreload
templates.env.filters["dateformat"] = dateformat

index = Index()
markdown = md.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
