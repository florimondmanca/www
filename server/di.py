from typing import TypeVar

from .application.parsers import Parser
from .domain.repositories import CategoryRepository, PageRepository
from .infrastructure.di import Container
from .seedwork.domain.cqrs import MessageBus
from .seedwork.infrastructure.cqrs import AsyncBus

T = TypeVar("T")


def _configure(container: Container) -> None:
    from .infrastructure import module
    from .infrastructure.database import PageDatabase
    from .infrastructure.parsers import MarkdownParser
    from .infrastructure.repositories import (
        FixedCategoryRepository,
        InMemoryPageRepository,
    )
    from .web.reload import HotReload
    from .web.templating import Templates

    bus = AsyncBus(query_handlers=module.query_handlers)
    container.register(MessageBus, instance=bus)

    container.register(Parser, instance=MarkdownParser())

    page_db = PageDatabase()
    container.register(PageDatabase, instance=page_db)

    container.register(PageRepository, instance=InMemoryPageRepository(page_db))
    container.register(CategoryRepository, instance=FixedCategoryRepository())

    hotreload = HotReload(page_db)
    container.register(HotReload, instance=hotreload)

    container.register(Templates, instance=Templates(hotreload))


def create_container() -> Container:
    return Container(_configure)


_container = create_container()

bootstrap = _container.bootstrap
resolve = _container.resolve
