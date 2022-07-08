import httpx


def to_production_url(url: str) -> str:
    urlobj = httpx.URL(url)
    return str(urlobj.copy_with(scheme="https", host="florimond.dev", port=None))
