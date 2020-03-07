from . import settings


def is_static_asset(path: str) -> bool:
    if path.startswith(settings.STATIC_ROOT):
        return True

    _, _, suffix = path.rpartition("/")
    _, has_extension, _ = suffix.partition(".")
    if has_extension:
        return True

    return False
