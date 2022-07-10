from dataclasses import dataclass

from ..domain.entities import Page
from ..seedwork.domain.cqrs import Query
from .sources import ContentItem


@dataclass
class GetPages(Query[list[Page]]):
    items: list[ContentItem]
