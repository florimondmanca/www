from typing import TypeVar

import httpx

from . import settings
from .domain.repositories import BuildReportRepository
from .infrastructure.cache import DiskCache
from .infrastructure.di import Container
from .infrastructure.webdav import BuildReportClient

T = TypeVar("T")


def _configure(container: Container) -> None:
    from .infrastructure.database import InMemoryDatabase
    from .infrastructure.repositories import InMemoryBuildReportRepository
    from .web.reload import HotReload
    from .web.templating import Templates

    db = InMemoryDatabase()
    container.register(InMemoryDatabase, instance=db)

    hotreload = HotReload()
    container.register(HotReload, instance=hotreload)

    container.register(Templates, instance=Templates(hotreload))

    container.register(
        BuildReportRepository, instance=InMemoryBuildReportRepository(db)
    )
    container.register(
        BuildReportClient,
        instance=BuildReportClient(
            username=settings.WEBDAV_USERNAME,
            password=str(settings.WEBDAV_PASSWORD),
            cache=DiskCache(directory=settings.BUILD_REPORTS_CACHE_DIR),
        ),
    )


def create_container() -> Container:
    return Container(_configure)


_container = create_container()

bootstrap = _container.bootstrap
resolve = _container.resolve
