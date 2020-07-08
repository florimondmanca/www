import arel

from . import content

hotreload = arel.HotReload(
    paths=[
        arel.Path("./content", on_reload=[content.load_content]),
        arel.Path("./server/templates"),
        arel.Path("./server/static"),
    ]
)
