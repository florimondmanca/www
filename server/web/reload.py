import arel

from .. import settings
from ..infrastructure.database import PageDatabase


class HotReload(arel.HotReload):
    def __init__(self, page_db: PageDatabase) -> None:
        super().__init__(
            paths=[
                arel.Path("./content", on_reload=[page_db.reload]),
                *(
                    arel.Path(str(d), on_reload=[page_db.reload])
                    for d in settings.EXTRA_CONTENT_DIRS
                ),
                arel.Path("./server/web/templates"),
                arel.Path("./server/web/static"),
            ]
        )
