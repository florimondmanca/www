from typing import List

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from .locale import Locale


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

    def _get_language(self, request: Request) -> str:
        for language in self._languages:
            language_prefix = f"/{language}"
            if request.url.path.startswith(language_prefix):
                return language

        try:
            return request.headers["Accept-Language"]
        except KeyError:
            pass

        return self._default_language

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        language = self._get_language(request)

        if language in self._languages:
            Locale.set(language)

        return await call_next(request)
