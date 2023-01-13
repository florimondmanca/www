import arel

from .. import settings
from ..infrastructure.database import InMemoryDatabase


class HotReload(arel.HotReload):
    def __init__(self, db: InMemoryDatabase) -> None:
        super().__init__(
            paths=[
                arel.Path("./content", on_reload=[db.reload]),
                *(
                    arel.Path(str(d), on_reload=[db.reload])
                    for d in settings.EXTRA_CONTENT_DIRS
                ),
                arel.Path("./server/web/templates"),
                arel.Path("./server/web/static"),
            ]
        )
