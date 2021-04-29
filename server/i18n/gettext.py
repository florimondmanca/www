from babel.support import LazyProxy

from .locale import get_locale


def gettext(message: str) -> str:
    locale = get_locale()
    return locale.gettext(message)


def ngettext(singular: str, plural: str, count: int) -> str:
    raise NotImplementedError  # pragma: no cover


def gettext_lazy(string: str) -> LazyProxy:
    return LazyProxy(gettext, string, enable_cache=False)
