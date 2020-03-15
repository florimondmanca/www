import asyncio
import logging
import os
from typing import Callable, Dict, Iterator, Optional, Sequence

logger = logging.getLogger(__name__)


class PathReload:
    CHECK_INTERVAL = 0.5

    def __init__(
        self,
        iter_paths: Callable[[], Iterator[str]],
        on_reload: Sequence[Callable],
        interval: float = 0.5,
    ) -> None:
        self.iter_paths = iter_paths
        self.on_reload = on_reload
        self.interval = interval
        self.task: Optional[asyncio.Task] = None
        self.stat_check = StatCheck()

    async def startup(self) -> None:
        assert self.task is None
        self.task = asyncio.create_task(self._main())

    async def _main(self) -> None:
        while True:
            await asyncio.sleep(self.interval)
            await self._check_changes()

    def _find_changed(self) -> Optional[str]:
        for path in self.iter_paths():
            if self.stat_check.check_changed(path):
                return path
        return None

    async def _check_changes(self) -> None:
        path = self._find_changed()
        if path is None:
            return

        logger.warning("Detected file change in %r. Reloading...", path)

        for callback in self.on_reload:
            await callback()

        self.stat_check.reset()

    async def shutdown(self) -> None:
        assert self.task is not None
        self.task.cancel()


class StatCheck:
    def __init__(self) -> None:
        self.last_modified: Dict[str, float] = {}

    def check_changed(self, path: str) -> bool:
        try:
            last_modified = os.path.getmtime(path)
        except OSError:
            return False

        old_last_modified = self.last_modified.get(path)

        if old_last_modified is None:
            self.last_modified[path] = last_modified
            return False

        if last_modified <= old_last_modified:
            return False

        return True

    def reset(self) -> None:
        self.last_modified = {}
