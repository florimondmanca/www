from typing import Any

import httpx

from ..domain.entities import Post, Category, Keyword


def to_production_url(url: str) -> str:
    urlobj = httpx.URL(url)
    return str(urlobj.copy_with(scheme="https", host="florimond.dev", port=None))


def get_absolute_url(obj: Any) -> str:
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
