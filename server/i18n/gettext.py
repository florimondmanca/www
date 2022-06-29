from asgi_babel import gettext, ngettext
from babel.support import LazyProxy

__all__ = ["gettext", "ngettext", "gettext_lazy"]


def gettext_lazy(string: str) -> LazyProxy:
    return LazyProxy(gettext, string, enable_cache=False)
