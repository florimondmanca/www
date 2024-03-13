from typing import Any

import httpx

from .. import settings
from ..domain.entities import BuildReport


def to_production_url(url: str) -> str:
    urlobj = httpx.URL(url)

    scheme, host, port = (
        ("http", f"localhost", settings.PORT)
        if settings.DEBUG
        else ("http" if settings.TESTING else "https", f"florimond.dev", None)
    )

    path = "/diypedals" + urlobj.path

    return str(urlobj.copy_with(scheme=scheme, host=host, port=port, path=path))


def get_absolute_path(obj: Any) -> str:
    if isinstance(obj, BuildReport):
        return f"/build-reports/{obj.slug}"

    raise ValueError(f"No absolute URL defined for {obj!r}")
