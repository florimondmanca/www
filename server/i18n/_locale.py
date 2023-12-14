import logging
from contextvars import ContextVar

from babel.core import Locale as _Locale
from babel.support import NullTranslations, Translations

from .. import settings

logger = logging.getLogger("uvicorn.error")

# Load translations at import time, so that import-time calls to
# gettext_lazy are properly registered.
_translations = {
    lang: Translations.load(str(settings.LOCALE_DIR), [lang], settings.LOCALE_DOMAIN)
    for lang in settings.LOCALE_TRANSLATIONS
}
_supported_locales = {settings.DEFAULT_LANGUAGE, *_translations.keys()}

logger.info("Supported locales: %s", _supported_locales)


class Locale:
    """
    A convenience wrapper around a `gettext` translations object.
    """

    def __init__(
        self, language: str, translations: NullTranslations | None = None
    ) -> None:
        self._language = language
        self._translations = (
            translations if translations is not None else NullTranslations()
        )

    @property
    def language(self) -> str:
        return self._language

    def gettext(self, message: str) -> str:
        return self._translations.ugettext(message)

    def __repr__(self) -> str:
        return f"<Locale({self._language!r})>"


def build_locale(code: str) -> Locale:
    # 'Negotiate' deals with 'fr' -> 'fr_FR', etc.
    locale = _Locale.negotiate(preferred=[code], available=_supported_locales)

    if locale is None:  # pragma: no cover
        raise RuntimeError(f"Unsupported locale: {code!r}")

    return Locale(language=locale.language, translations=_translations.get(str(locale)))


_locale_context: ContextVar["Locale"] = ContextVar(
    "locale", default=build_locale(settings.DEFAULT_LANGUAGE)
)


def set_locale(code: str) -> None:
    locale = build_locale(code)
    logger.debug("set_locale locale=%s", locale)
    _locale_context.set(locale)


def get_locale() -> "Locale":
    return _locale_context.get()
