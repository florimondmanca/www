from typing import Any

from .gettext import gettext, ngettext


def setup_jinja2(env: Any) -> None:
    env.add_extension("jinja2.ext.i18n")
    env.install_gettext_callables(gettext, ngettext, newstyle=True)
