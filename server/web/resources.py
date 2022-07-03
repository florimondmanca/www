import datetime as dt

from starlette.exceptions import HTTPException
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from .. import settings
from ..content import get_category_label as category_label
from . import i18n
from .reload import hotreload

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
static = StaticFiles(directory=str(settings.STATIC_DIR))


def raise_server_error(message: str) -> None:  # pragma: no cover
    raise HTTPException(500, detail=message)


def dateformat(value: str) -> str:
    datevalue = dt.datetime.strptime(value, "%Y-%m-%d")
    return datevalue.strftime("%b %d, %Y")


def language_label(value: str) -> str:
    return settings.LANGUAGE_LABELS.get(value, value)


i18n.setup_jinja2(templates)

templates.env.globals["now"] = dt.datetime.now
templates.env.globals["raise"] = raise_server_error
templates.env.globals["settings"] = settings
templates.env.globals["hotreload"] = hotreload
templates.env.filters["dateformat"] = dateformat
templates.env.filters["category_label"] = category_label
templates.env.filters["language_label"] = language_label
