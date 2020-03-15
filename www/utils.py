import os
from pathlib import Path

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


def is_localhost(hostname: str) -> bool:
    return hostname in ("localhost", "127.0.0.1")


def get_display_path(filename: str) -> str:
    path = os.path.normpath(filename)
    if Path.cwd() in Path(filename).parents:
        path = os.path.normpath(os.path.relpath(filename))
    return path
