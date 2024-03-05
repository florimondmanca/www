from ..domain.entities import BuildReport
from ..domain.repositories import BuildReportRepository
from .database import InMemoryDatabase


class InMemoryBuildReportRepository(BuildReportRepository):
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    async def save(self, build_report: BuildReport) -> None:
        self._db.insert_build_report(build_report)

    async def find_all(self) -> list[BuildReport]:
        return self._db.find_all_build_reports()

    async def find_one(self, *, slug: str) -> BuildReport:
        return self._db.find_one_build_report(slug)
