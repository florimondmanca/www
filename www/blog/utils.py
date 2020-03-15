import glob
import os
from pathlib import Path
from typing import Dict, Iterable, Iterator, Optional


def find_markdown_files(root: Path) -> Iterator[Path]:
    pattern = str(root / "**" / "*.md")
    for path in glob.glob(pattern, recursive=True):
        yield Path(path)


class StatReload:
    def __init__(self) -> None:
        self.last_modified: Dict[str, float] = {}

    def find_changed(self, paths: Iterable[str]) -> Optional[str]:
        for path in paths:
            try:
                last_modified = os.path.getmtime(path)
            except OSError:
                continue

            old_last_modified = self.last_modified.get(path)

            if old_last_modified is None:
                self.last_modified[path] = last_modified
                continue

            if last_modified <= old_last_modified:
                continue

            return path

        return None

    def reset(self) -> None:
        self.last_modified = {}
