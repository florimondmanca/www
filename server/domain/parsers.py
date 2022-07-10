from .entities import Metadata


class Parser:
    def parse(self, raw: str) -> tuple[str, Metadata]:
        raise NotImplementedError  # pragma: no cover
