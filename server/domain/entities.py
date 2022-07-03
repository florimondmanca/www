import dataclasses
import re
from typing import List, Optional

PRIVATE_RE = re.compile(r"prv-\d+$")


@dataclasses.dataclass(frozen=True)
class ContentItem:
    content: str
    location: str


@dataclasses.dataclass(frozen=True)
class Frontmatter:
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None
    image: Optional[str] = None
    image_thumbnail: Optional[str] = None
    image_caption: Optional[str] = None
    tags: List[str] = dataclasses.field(default_factory=list)
    tag: Optional[str] = None


@dataclasses.dataclass(frozen=True)
class Page:
    permalink: str
    frontmatter: Frontmatter
    meta: List[dict]
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
