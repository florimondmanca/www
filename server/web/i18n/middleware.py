from typing import List

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from server.i18n import set_locale


class LocaleMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        languages: List[str],
        default_language: str,
    ) -> None:
        super().__init__(app)
        self._languages = languages
        self._default_language = default_language

    def _get_language_from_path(self, path: str) -> str:
        for language in self._languages:
            language_prefix = f"/{language}"
            if path.startswith(language_prefix):
                return language

        return self._default_language

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        language = self._get_language_from_path(request.url.path)
        assert language in self._languages
        set_locale(language)
        request.scope["language"] = language  # For usage by routes.
        return await call_next(request)
