import glob
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator

import aiofiles
from starlette.concurrency import run_in_threadpool

from .. import settings


@dataclass
class ContentItem:
    source: "ContentSource"
    location: Path


class ContentSource:
    async def get(self) -> str:
        raise NotImplementedError  # pragma: no cover


class FileContentSource(ContentSource):
    def __init__(self, path: Path) -> None:
        self._path = path

    async def get(self) -> str:
        async with aiofiles.open(self._path) as f:
            return await f.read()


async def load_content_items() -> list[ContentItem]:
    items = []

    async for root, path in aiter_content_paths():
        item = ContentItem(
            location=path.relative_to(root),
            source=FileContentSource(path),
        )
        items.append(item)

    return items


async def aiter_content_paths() -> AsyncIterator[tuple[Path, Path]]:
    content_dirs = [settings.CONTENT_DIR, *settings.EXTRA_CONTENT_DIRS]

    for root in content_dirs:
        pattern = str(root / "**" / "*.md")
        globbed = await run_in_threadpool(
            glob.glob, pattern, recursive=True  # type: ignore
        )
        for path in globbed:
            yield (root, Path(str(path)))
