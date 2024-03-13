import datetime as dt
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Kit:
    name: str
    seller: str
    url: str


@dataclass(frozen=True)
class Pcb:
    name: str
    seller: str
    url: str


@dataclass(frozen=True)
class Photo:
    src: str
    alt: str


@dataclass(frozen=True)
class BuildReport:
    title: str
    slug: str
    description: str
    categories: list[str]
    build_date: dt.date
    status: str
    photos: list[Photo] = field(default_factory=list)
    kit: Kit | None = None
    pcb: Pcb | None = None
