from .entities import BuildReport


class BuildReportRepository:
    async def save(self, build_report: BuildReport) -> None:
        raise NotImplementedError  # pragma: no cover

    async def find_all(self) -> list[BuildReport]:
        raise NotImplementedError  # pragma: no cover

    async def find_one(self, *, slug: str) -> BuildReport:
        raise NotImplementedError  # pragma: no cover
