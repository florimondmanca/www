from babel.support import LazyProxy

from .locale import Locale


def gettext(message: str) -> str:
    locale = Locale.get()
    return locale.gettext(message)


def ngettext(singular: str, plural: str, count: int) -> str:
    raise NotImplementedError  # pragma: no cover


def gettext_lazy(string: str) -> LazyProxy:
    return LazyProxy(gettext, string, enable_cache=False)
