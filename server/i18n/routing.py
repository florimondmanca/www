# from typing import Any, Tuple
from typing import Tuple

from starlette import status
from starlette.datastructures import URL, Scope, URLPath
from starlette.responses import RedirectResponse
from starlette.routing import Match, Route
from starlette.types import Receive, Send

from .. import settings
from .locale import Locale


class LocaleRoute(Route):
    def matches(self, scope: Scope) -> Tuple[Match, Scope]:
        if scope["type"] != "http":
            # Eg hot-reload WebSocket.
            return super().matches(scope)

        # Drop any language prefix for matching.
        # For example, LocaleRoute("/blog") should match "/fr/blog".
        path = scope["path"]
        for language in settings.LANGUAGES:
            language_prefix = f"/{language}"
            if path.startswith(language_prefix):
                scope = {**scope, "path": path[len(language_prefix) :]}
                break
        else:
            # If no language prefix is present, assume redirection to default language.
            scope["redirect_default_language"] = True

        return super().matches(scope)

    def url_path_for(self, name: str, **path_params: str) -> URLPath:
        # Automatically prepend language prefix to reversed URLs.
        # Accept magic 'lang' path parameter to set language
        # explicitly: `url_for(..., lang=...)`.
        language = path_params.pop("lang", Locale.get().language)
        url_path = super().url_path_for(name, **path_params)
        return URLPath(f"/{language}{url_path}")

    async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        if "redirect_default_language" in scope:
            # Example: '/blog/...' -> '/en/blog/...'
            prefix = f"/{settings.DEFAULT_LANGUAGE}"
            redirect_path = prefix + scope["path"]
            response = RedirectResponse(
                URL(scope=scope).replace(path=redirect_path),
                status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            )
            await response(scope, receive, send)
            return

        await super().handle(scope, receive, send)
