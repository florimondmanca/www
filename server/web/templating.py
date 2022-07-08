import datetime as dt

import jinja2
from starlette.exceptions import HTTPException
from starlette.templating import Jinja2Templates

from .. import settings
from ..infrastructure.pages import get_category_label as category_label
from . import i18n
from .reload import HotReload


class Templates(Jinja2Templates):
    def __init__(self, hotreload: HotReload) -> None:
        super().__init__(directory=str(settings.TEMPLATES_DIR))

        i18n.setup_jinja2(self)

        self.env.globals["now"] = dt.datetime.now
        self.env.globals["raise"] = self._raise_server_error
        self.env.globals["settings"] = settings
        self.env.globals["hotreload"] = hotreload
        self.env.filters["dateformat"] = self._dateformat
        self.env.filters["category_label"] = category_label
        self.env.filters["language_label"] = self._language_label

    @staticmethod
    def _raise_server_error(message: str) -> None:  # pragma: no cover
        raise HTTPException(500, detail=message)

    @staticmethod
    def _dateformat(value: str) -> str:
        datevalue = dt.datetime.strptime(value, "%Y-%m-%d")
        return datevalue.strftime("%b %d, %Y")

    @staticmethod
    def _language_label(value: str) -> str:
        return settings.LANGUAGE_LABELS.get(value, value)

    def from_string(self, source: str) -> jinja2.Template:
        return self.env.from_string(source)
