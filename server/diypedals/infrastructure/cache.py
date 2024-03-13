import json
from pathlib import Path
from typing import Any, Callable


class DiskCache:
    def __init__(self, directory: Path) -> None:
        self._dir = directory
        self._dir.mkdir(exist_ok=True)
        self._file = self._dir / "cache.json"
        if not self._file.exists():
            self._file.write_text("{}")

    def _get_cache(self) -> dict:
        return json.loads(self._file.read_text())

    def _write_cache(self, cache: dict) -> None:
        self._file.write_text(json.dumps(cache))

    async def get(self, key: str, fetch_func: Callable) -> Any:
        cache = self._get_cache()

        try:
            return cache[key]
        except KeyError:
            value = await fetch_func()
            cache[key] = value
            self._write_cache(cache)
            return value
