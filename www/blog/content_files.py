from pathlib import Path
from typing import Iterator

from .utils import find_markdown_files


class ContentFiles:
    """
    Base interface for content files iterators.
    """

    def __iter__(self) -> Iterator[Path]:
        raise NotImplementedError  # pragma: no cover

    def relative(self, path: Path) -> Path:
        return path


class FilesystemContentFiles:
    """
    A content files iterator that searches through the filesystem.
    """

    def __init__(self, root: Path):
        self.root = root

    def __iter__(self) -> Iterator[Path]:
        yield from find_markdown_files(self.root)

    def relative(self, path: Path) -> Path:
        return path.relative_to(self.root)
