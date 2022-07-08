from typing import TypeVar

from .domain.repositories import PageRepository
from .infrastructure.database import PageDatabase
from .infrastructure.di import Container
from .infrastructure.repositories import InMemoryPageRepository
from .web.reload import HotReload
from .web.templating import Templates

T = TypeVar("T")


def _configure(container: Container) -> None:
    page_db = PageDatabase()
    container.register(PageDatabase, instance=page_db)

    container.register(PageRepository, instance=InMemoryPageRepository(page_db))

    hotreload = HotReload(page_db)
    container.register(HotReload, instance=hotreload)

    container.register(Templates, instance=Templates(hotreload))


def create_container() -> Container:
    return Container(_configure)


_container = create_container()

bootstrap = _container.bootstrap
resolve = _container.resolve
