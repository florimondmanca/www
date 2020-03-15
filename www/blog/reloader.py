import asyncio
import logging
from typing import Callable, Optional, Sequence

from ..utils import get_display_path
from . import content
from .utils import StatReload

logger = logging.getLogger(__name__)


class ContentReloader:
    CHECK_INTERVAL = 0.5

    def __init__(self, on_reload: Sequence[Callable], interval: float = 0.5) -> None:
        self.on_reload = on_reload
        self.interval = interval
        self.task: Optional[asyncio.Task] = None
        self.stat_reload = StatReload()

    async def check_changes(self) -> None:
        path = self.stat_reload.find_changed(
            str(path) for path in content.iter_content_paths()
        )
        if path is None:
            return

        message = "Detected file change in '%s'. Reloading..."
        logger.warning(message, get_display_path(path))

        for callback in self.on_reload:
            await callback()
        self.stat_reload.reset()

    async def main(self) -> None:
        while True:
            await asyncio.sleep(self.interval)
            await self.check_changes()

    async def start(self) -> None:
        assert self.task is None
        self.task = asyncio.create_task(self.main())

    async def stop(self) -> None:
        assert self.task is not None
        self.task.cancel()
