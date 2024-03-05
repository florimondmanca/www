from pathlib import Path

import arel

from .. import settings

HERE = Path(__file__).parent


class HotReload(arel.HotReload):
    def __init__(self) -> None:
        super().__init__(
            paths=[
                arel.Path(settings.TEMPLATES_DIR),
                arel.Path(settings.STATIC_DIR),
            ]
        )
