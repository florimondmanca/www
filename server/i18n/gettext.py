from babel.support import LazyProxy

from .locale import get_locale


def gettext(message: str) -> str:
    locale = get_locale()
    return locale.gettext(message)


def gettext_lazy(string: str) -> LazyProxy:
    return LazyProxy(gettext, string, enable_cache=False)
