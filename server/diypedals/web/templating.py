import datetime as dt
from typing import Any

import jinja2
from starlette.templating import Jinja2Templates

from .. import settings
from ..infrastructure.urls import get_absolute_path, to_production_url
from .reload import HotReload


class Templates(Jinja2Templates):
    def __init__(self, hotreload: HotReload) -> None:
        super().__init__(directory=str(settings.TEMPLATES_DIR))

        def _absolute_url(obj: Any) -> str:
            return to_production_url(get_absolute_path(obj))

        self.env.globals["now"] = dt.datetime.now
        self.env.globals["settings"] = settings
        self.env.globals["hotreload"] = hotreload
        self.env.filters["absolute_url"] = _absolute_url
        self.env.filters["dateformat"] = _dateformat
        self.env.filters["isoformat"] = lambda value: value.isoformat()

    def from_string(self, source: str) -> jinja2.Template:
        return self.env.from_string(source)


def _dateformat(value: dt.date | str) -> str:
    if isinstance(value, str):
        value = dt.date.fromisoformat(value)
    return value.strftime("%b %d, %Y")
