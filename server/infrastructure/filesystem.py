import glob
from dataclasses import dataclass
from pathlib import Path

import aiofiles

from .. import settings


@dataclass
class ContentItem:
    content: str
    location: Path


async def load_content_items() -> list[ContentItem]:
    items = []

    for root, path in iter_content_paths():
        async with aiofiles.open(path) as f:
            content = await f.read()
            item = ContentItem(
                content=content,
                location=path.relative_to(root),
            )
            items.append(item)

    return items


def iter_content_paths() -> list[tuple[Path, Path]]:
    content_dirs = [settings.CONTENT_DIR, *settings.EXTRA_CONTENT_DIRS]
    paths = []

    for root in content_dirs:
        pattern = str(root / "**" / "*.md")
        for path in glob.glob(pattern, recursive=True):
            paths.append((root, Path(path)))

    return paths
