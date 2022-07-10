import dataclasses
import re
from dataclasses import dataclass
from typing import List, Optional

PRIVATE_RE = re.compile(r"prv-\d+$")


@dataclass(frozen=True)
class Tag:
    slug: str

    def __str__(self) -> str:
        return self.slug


@dataclasses.dataclass(frozen=True)
class Metadata:
    title: str = ""
    description: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None
    image: Optional[str] = None
    image_thumbnail: Optional[str] = None
    image_caption: Optional[str] = None
    tags: List[Tag] = dataclasses.field(default_factory=list)
    tag: Optional[Tag] = None


@dataclasses.dataclass(frozen=True)
class Page:
    permalink: str
    metadata: Metadata
    html: str = ""
    content: str = ""

    @property
    def language(self) -> str:
        # '/en/posts/...' -> 'en'
        parts = self.permalink.split("/")
        return parts[1]

    @property
    def is_post(self) -> bool:
        return "/posts/" in self.permalink

    @property
    def is_category(self) -> bool:
        return "/category/" in self.permalink

    @property
    def is_private(self) -> bool:
        return PRIVATE_RE.search(self.permalink) is not None
