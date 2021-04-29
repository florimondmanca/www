from typing import Tuple

from starlette.datastructures import Scope
from starlette.routing import Match, Route


class LocaleRoute(Route):
    def matches(self, scope: Scope) -> Tuple[Match, Scope]:
        if scope["type"] != "http":  # pragma: no cover
            # Eg hot-reload WebSocket.
            return super().matches(scope)

        path = scope["path"]
        assert "language" in scope, "LocaleMiddleware is not installed"
        language = scope["language"]

        # Let route match regardless of language prefix.
        # Example: a request to "/fr/blog" should match `LocaleRoute("/blog")`.

        language_prefix = f"/{language}"
        if not path.startswith(language_prefix):
            # Unknown languages are passed through and result
            # in a "no-match", as expected.
            return super().matches(scope)

        # Don't normalize in-place to avoid interferring with
        # matching of other routes.
        normalized_scope = {**scope, "path": path[len(language_prefix) :]}

        return super().matches(normalized_scope)
