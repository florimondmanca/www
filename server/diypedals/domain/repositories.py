from .entities import BuildReport


class BuildReportRepository:
    async def save(self, build_report: BuildReport) -> None:
        raise NotImplementedError  # pragma: no cover

    async def find_all(self, *, category: str | None = None) -> list[BuildReport]:
        raise NotImplementedError  # pragma: no cover

    async def find_one(self, *, slug: str) -> BuildReport | None:
        raise NotImplementedError  # pragma: no cover

    async def get_unique_categories(self) -> dict[str, int]:
        raise NotImplementedError  # pragma: no cover

    async def find_all_with_category(self, category: str) -> list[BuildReport]:
        raise NotImplementedError  # pragma: no cover
