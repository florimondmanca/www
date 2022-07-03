import datetime as dt

import markdown as md
from starlette.exceptions import HTTPException
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import i18n, settings
from .domain.repositories import PageRepository
from .reload import hotreload

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
static = StaticFiles(directory=str(settings.STATIC_DIR))


def raise_server_error(message: str) -> None:  # pragma: no cover
    raise HTTPException(500, detail=message)


def dateformat(value: str) -> str:
    datevalue = dt.datetime.strptime(value, "%Y-%m-%d")
    return datevalue.strftime("%b %d, %Y")


def category_label(value: str) -> str:
    from .content import get_category_label  # Avoid circular import.

    return get_category_label(value)


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

page_repository = PageRepository()

markdown = md.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
