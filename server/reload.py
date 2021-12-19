import arel

from . import settings


async def on_reload() -> None:  # pragma: no cover
    from . import content  # Avoid circular imports.

    await content.load_content()


hotreload = arel.HotReload(
    paths=[
        arel.Path("./content", on_reload=[on_reload]),
        *(
            arel.Path(str(d), on_reload=[on_reload])
            for d in settings.EXTRA_CONTENT_DIRS
        ),
        arel.Path("./server/templates"),
        arel.Path("./server/static"),
    ]
)
