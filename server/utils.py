import httpx

from . import settings


def is_static_asset(path: str) -> bool:
    if not path.endswith("/"):
        path = f"{path}/"

    if path.startswith(f"{settings.STATIC_ROOT}/"):
        return True

    _, _, suffix = path.rstrip("/").rpartition("/")
    _, has_extension, _ = suffix.partition(".")
    if has_extension:
        return True

    return False


def to_production_url(url: str) -> str:
    urlobj = httpx.URL(url)
    return str(urlobj.copy_with(scheme="https", host="florimond.dev", port=None))
