from . import i18n, settings

i18n.load_translations(
    directory=str(settings.LOCALES_DIR),
    domain=settings.LOCALES_DOMAIN,
)

from .app import app  # noqa: E402

__all__ = ["app"]
