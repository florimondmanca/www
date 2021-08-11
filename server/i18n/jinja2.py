from starlette.templating import Jinja2Templates

from .gettext import gettext, ngettext
from .locale import get_locale


def i18n_path(path: str) -> str:
    language = get_locale().language
    return f"/{language}{path}"


def setup_jinja2(templates: Jinja2Templates) -> None:
    templates.env.add_extension("jinja2.ext.i18n")
    templates.env.install_gettext_callables(  # type: ignore
        gettext, ngettext, newstyle=True
    )
    templates.env.globals["i18n_path"] = i18n_path
