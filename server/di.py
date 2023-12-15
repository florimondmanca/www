from typing import TypeVar

from .domain.repositories import CategoryRepository, KeywordRepository, PostRepository
from .infrastructure.di import Container
from .infrastructure.markdown import MarkdownParser

T = TypeVar("T")


def _configure(container: Container) -> None:
    from .infrastructure.database import InMemoryDatabase
    from .infrastructure.repositories import (
        InMemoryCategoryRepository,
        InMemoryKeywordRepository,
        InMemoryPostRepository,
    )
    from .web.reload import HotReload
    from .web.templating import Templates

    container.register(MarkdownParser, instance=MarkdownParser())

    db = InMemoryDatabase()
    container.register(InMemoryDatabase, instance=db)

    container.register(PostRepository, instance=InMemoryPostRepository(db))
    container.register(CategoryRepository, instance=InMemoryCategoryRepository(db))
    container.register(KeywordRepository, instance=InMemoryKeywordRepository(db))

    hotreload = HotReload(db)
    container.register(HotReload, instance=hotreload)

    container.register(Templates, instance=Templates(hotreload))


def create_container() -> Container:
    return Container(_configure)


_container = create_container()

bootstrap = _container.bootstrap
resolve = _container.resolve
