import datetime as dt

import jinja2
from starlette.exceptions import HTTPException
from starlette.templating import Jinja2Templates

from .. import settings
from ..infrastructure.html import build_meta_tags
from ..infrastructure.urls import get_absolute_url
from . import i18n
from .reload import HotReload


class Templates(Jinja2Templates):
    def __init__(self, hotreload: HotReload) -> None:
        super().__init__(directory=str(settings.TEMPLATES_DIR))

        i18n.setup_jinja2(self)

        self.env.globals["now"] = dt.datetime.now
        self.env.globals["raise"] = _raise_server_error
        self.env.globals["settings"] = settings
        self.env.globals["hotreload"] = hotreload
        self.env.filters["absolute_url"] = get_absolute_url
        self.env.filters["dateformat"] = _dateformat
        self.env.filters["language_label"] = _language_label
        self.env.filters["meta_tags"] = build_meta_tags

    def from_string(self, source: str) -> jinja2.Template:
        return self.env.from_string(source)


def _raise_server_error(message: str) -> None:  # pragma: no cover
    raise HTTPException(500, detail=message)


def _dateformat(value: dt.date | str) -> str:
    if isinstance(value, str):
        value = dt.date.fromisoformat(value)
    return value.strftime("%b %d, %Y")


def _language_label(value: str) -> str:
    return settings.LANGUAGE_LABELS.get(value, value)
