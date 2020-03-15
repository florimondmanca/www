import logging
import os
from pathlib import Path
from typing import Iterator, Sequence, Union

from . import settings

logger = logging.getLogger(__name__)


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


def iter_files_with_extensions(
    extensions: Sequence[str], directories: Sequence[Union[Path, str]]
) -> Iterator[str]:
    extensions = tuple(extensions)
    for directory in directories:
        for subdir, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(extensions):
                    yield os.path.join(subdir, filename)


def get_display_path(filename: str) -> str:
    path = os.path.normpath(filename)
    if Path.cwd() in Path(filename).parents:
        path = os.path.normpath(os.path.relpath(filename))
    return path
