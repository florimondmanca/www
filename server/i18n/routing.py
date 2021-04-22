from typing import Tuple

from starlette.datastructures import Scope
from starlette.routing import Match, Route


class LocaleRoute(Route):
    def matches(self, scope: Scope) -> Tuple[Match, Scope]:
        if scope["type"] != "http":
            # Eg hot-reload WebSocket.
            return super().matches(scope)

        path = scope["path"]
        assert "language" in scope, "LocaleMiddleware is not installed"
        language = scope["language"]

        # Let route match regardless of language prefix.
        # Example: a request to "/fr/blog" should match `LocaleRoute("/blog")`.
        # NOTE: Unknown languages are passed through and result
        # in a "no-match", as expected.
        language_prefix = f"/{language}"
        if path.startswith(language_prefix):
            scope["path"] = path[len(language_prefix) :]

        return super().matches(scope)
