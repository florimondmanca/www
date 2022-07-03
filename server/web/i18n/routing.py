from typing import Tuple

from starlette.datastructures import Scope
from starlette.routing import Match, Route, URLPath

from server.i18n import get_locale


class LocaleRoute(Route):
    def matches(self, scope: Scope) -> Tuple[Match, Scope]:
        if scope["type"] != "http":  # pragma: no cover
            # Eg hot-reload WebSocket.
            return super().matches(scope)

        path = scope["path"]
        assert "language" in scope, "LocaleMiddleware is not installed"
        language = scope["language"]

        # Let route match regardless of language prefix.
        # Example: a request to "/fr/xyz" should match `LocaleRoute("/xyz")`.

        language_prefix = f"/{language}"
        if not path.startswith(language_prefix):
            # Unknown languages are passed through and result
            # in a "no-match", as expected.
            return super().matches(scope)

        # Don't normalize in-place to avoid interferring with
        # matching of other routes.
        normalized_scope = {**scope, "path": path[len(language_prefix) :]}

        return super().matches(normalized_scope)

    def url_path_for(self, name: str, **path_params: str) -> URLPath:
        # Allow `url_for(..., language=...)`
        language = path_params.pop("language", None)

        url_path = super().url_path_for(name, **path_params)

        # Default to active language if not passed as path param.
        if language is None:
            locale = get_locale()
            language = locale.language

        # Prepend language prefix
        # Eg given LocaleRoute("/", name="home") and language="fr",
        # url_for('home') would return "/fr/" (rather than "/").
        language_prefix = f"/{language}"
        assert not url_path.startswith(language_prefix)

        return URLPath(f"{language_prefix}{url_path}")
