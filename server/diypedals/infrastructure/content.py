from .. import settings
from ..di import resolve
from ..domain.repositories import BuildReportRepository
from .cache import DiskCache
from .webdav import BuildReportClient


async def load_build_reports() -> None:
    repository = resolve(BuildReportRepository)
    client = resolve(BuildReportClient)

    async for build_report in client.fetch_all():
        await repository.save(build_report)
