from ..domain.entities import BuildReport
from ..domain.repositories import BuildReportRepository
from .database import InMemoryDatabase


class InMemoryBuildReportRepository(BuildReportRepository):
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    async def save(self, build_report: BuildReport) -> None:
        self._db.insert_build_report(build_report)

    async def find_all(self, *, category: str | None = None) -> list[BuildReport]:
        return self._db.find_all_build_reports(category=category)

    async def find_one(self, *, slug: str) -> BuildReport | None:
        return self._db.find_one_build_report(slug)

    async def get_unique_categories(self) -> dict[str, int]:
        return self._db.find_unique_build_report_categories()
