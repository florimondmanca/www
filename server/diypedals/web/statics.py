from typing import Any

from starlette.responses import Response
from starlette.staticfiles import StaticFiles


class CachedStaticFiles(StaticFiles):
    def __init__(self, *args: Any, max_age: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._max_age = max_age

    def file_response(self, *args: Any, **kwargs: Any) -> Response:
        response = super().file_response(*args, **kwargs)

        # Cache all static assets.
        response.headers.append("Cache-Control", f"public, max-age={self._max_age}")
        response.headers.append("Vary", "Accept-Encoding, User-Agent, Cookie, Referer")

        return response
