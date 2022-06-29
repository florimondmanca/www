from contextlib import contextmanager
from typing import Iterator

from asgi_babel import current_locale
from babel.core import Locale as _Locale

from .. import settings


def get_locale() -> _Locale:
    return current_locale.get() or _Locale.parse(settings.DEFAULT_LANGUAGE, sep="-")


def set_locale(lang: str) -> None:
    loc = _Locale.parse(lang, sep="-")
    current_locale.set(loc)


@contextmanager
def using_locale(lang: str) -> Iterator[None]:
    initial = get_locale().language
    set_locale(lang)
    try:
        yield
    finally:
        set_locale(initial)
