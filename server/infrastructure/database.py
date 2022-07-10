import collections
import itertools

from ..application.queries import GetPages
from ..di import resolve
from ..domain.entities import Page
from ..i18n import using_locale
from ..seedwork.domain.cqrs import MessageBus
from .sources import find_content_items


class PageDatabase:
    def __init__(self) -> None:
        self._store: dict[str, dict[str, Page]] = collections.defaultdict(dict)

    async def connect(self) -> None:
        await self._load()

    async def reload(self) -> None:
        await self._load()  # pragma: no cover

    async def _load(self) -> None:
        bus = resolve(MessageBus)

        items = await find_content_items()

        for language, language_items in itertools.groupby(
            items, key=lambda item: item.location.parts[0]
        ):
            with using_locale(language):
                pages = await bus.execute(GetPages(items=list(language_items)))
                for page in pages:
                    assert page.language == language
                    self._store[page.language][page.permalink] = page

    def find_one(self, language: str, permalink: str) -> Page | None:
        return self._store[language].get(permalink)

    def find_all(self, language: str) -> list[Page]:
        return list(self._store[language].values())
