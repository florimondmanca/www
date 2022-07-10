from dataclasses import dataclass
from pathlib import Path


@dataclass
class ContentItem:
    source: "ContentSource"
    location: Path


class ContentSource:
    async def get(self) -> str:
        raise NotImplementedError  # pragma: no cover
