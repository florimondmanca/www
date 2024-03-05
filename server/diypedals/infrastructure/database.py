from contextlib import contextmanager
from typing import Iterator

from .. import settings
from ..domain.entities import BuildReport
from .content import load_build_reports


class _Data:
    def __init__(self) -> None:
        self.build_reports: dict[str, BuildReport] = {}


class InMemoryDatabase:
    def __init__(self) -> None:
        self._data = _Data()

    async def connect(self) -> None:
        await self._load()

    async def reload(self) -> None:
        await self._load()  # pragma: no cover

    @contextmanager
    def isolated(self) -> Iterator[None]:
        previous_data = self._data
        self._data = _Data()
        try:
            yield
        finally:
            self._data = previous_data

    async def _load(self) -> None:
        self._data = _Data()

        await load_build_reports()

    def find_all_build_reports(self) -> list[BuildReport]:
        return sorted(
            self._data.build_reports.values(),
            key=lambda build_report: build_report.build_date,
            reverse=True,
        )

    def find_one_build_report(self, slug: str) -> BuildReport | None:
        return self._data.build_reports.get(slug)

    def insert_build_report(self, build_report: BuildReport) -> None:
        self._data.build_reports[build_report.slug] = build_report
