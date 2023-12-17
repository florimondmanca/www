from typing import Any

import httpx

from .. import settings
from ..domain.entities import Category, Keyword, Post


def to_production_url(url: str) -> str:
    urlobj = httpx.URL(url)

    scheme, host, port = (
        ("http", "localhost", settings.PORT)
        if settings.DEBUG
        else ("http" if settings.TESTING else "https", "florimond.dev", None)
    )

    return str(urlobj.copy_with(scheme=scheme, host=host, port=port))


def get_absolute_path(obj: Any) -> str:
    if isinstance(obj, Post):
        return (
            f"/{obj.in_language}"
            "/posts"
            f"/{obj.date_published.year}"
            f"/{obj.date_published.month:02}"
            f"/{obj.slug}"
        )

    if isinstance(obj, Category):
        return f"/{obj.in_language}/category/{obj.slug}"

    if isinstance(obj, Keyword):
        return f"/{obj.in_language}/tag/{obj.slug}"

    raise ValueError(f"No absolute URL defined for {obj!r}")
