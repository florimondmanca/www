import logging
import os
from contextvars import ContextVar
from typing import Dict, Set, Union

from babel.core import Locale as _Locale
from babel.core import negotiate_locale
from babel.support import NullTranslations, Translations

from .. import settings

logger = logging.getLogger("uvicorn.error")


class _GettextTranslations:
    def __init__(self, default: str) -> None:
        self._default = default
        self._translations: Dict[str, Union[Translations, NullTranslations]] = {}
        self._supported_locales: Set[str] = set()

    @property
    def translations(
        self,
    ) -> Dict[str, Union[Translations, NullTranslations]]:
        return self._translations

    @property
    def supported_locales(self) -> Set[str]:
        return self._supported_locales

    @property
    def default_locale(self) -> str:
        return self._default

    def load(self, directory: str, domain: str) -> None:
        for lang in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, lang)):
                continue
            translation = Translations.load(directory, [lang], domain)
            assert lang not in self._translations
            self._translations[lang] = translation

        self._supported_locales = set(self._translations.keys())
        self._supported_locales.add(self.default_locale)

        logger.info("Supported locales: %s", sorted(self._supported_locales))


_GETTEXT_TRANSLATIONS = _GettextTranslations(default=settings.DEFAULT_LANGUAGE)


def load_translations(directory: str, domain: str) -> None:
    _GETTEXT_TRANSLATIONS.load(directory, domain)


class Locale(_Locale):
    _LANGUAGE_CTX: ContextVar["Locale"] = ContextVar("language")
    _DEFAULT = _GETTEXT_TRANSLATIONS.default_locale

    @classmethod
    def _make(cls, code: str) -> "Locale":
        # Eg 'fr' should be negotiated as 'fr_FR'
        # NOTE: don't use `cls.negotiate()` as it returns a hardcoded
        # Babel `Locale` instance.
        identifier = negotiate_locale(
            preferred=[code],
            available=_GETTEXT_TRANSLATIONS.supported_locales,
        )
        if identifier is None:
            raise RuntimeError("Unsupported locale: {code!r}")  # pragma: no cover

        locale = cls.parse(identifier)
        translations = _GETTEXT_TRANSLATIONS.translations.get(
            identifier, NullTranslations()
        )
        locale.translations = translations

        return locale

    def gettext(self, message: str) -> str:
        return self.translations.ugettext(message)

    @classmethod
    def get(cls) -> "Locale":
        try:
            return cls._LANGUAGE_CTX.get()
        except LookupError:
            return cls._make(cls._DEFAULT)

    @classmethod
    def set(cls, code: str) -> None:
        locale = cls._make(code)
        logger.debug("Locale.set locale=%s", locale)
        cls._LANGUAGE_CTX.set(locale)
