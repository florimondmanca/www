import os
from typing import Dict


class FileChangeDetector:
    def has_changed(self, filename: str) -> bool:
        raise NotImplementedError  # pragma: no cover

    def reset(self) -> None:
        pass


class FilesystemFileChangeDetector:
    def __init__(self) -> None:
        self.last_modified: Dict[str, float] = {}

    def has_changed(self, filename: str) -> bool:
        try:
            last_modified = os.path.getmtime(filename)
        except OSError:
            return False

        old_last_modified = self.last_modified.get(filename)

        if old_last_modified is None:
            self.last_modified[filename] = last_modified
            return False

        if last_modified <= old_last_modified:
            return False

        return True

    def reset(self) -> None:
        self.last_modified = {}
