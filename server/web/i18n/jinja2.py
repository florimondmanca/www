from starlette.templating import Jinja2Templates

from server.i18n import gettext, ngettext


def setup_jinja2(templates: Jinja2Templates) -> None:
    templates.env.add_extension("jinja2.ext.i18n")
    templates.env.install_gettext_callables(  # type: ignore
        gettext, ngettext, newstyle=True
    )
