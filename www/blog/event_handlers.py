from .. import resources, settings
from . import content
from .reload import PathReload

on_startup = [content.load_content]
on_shutdown = []

if settings.DEBUG:

    async def notify_reload() -> None:
        channel = settings.BLOG_RELOAD_CHANNEL
        await resources.broadcast.publish(channel, message="reload")

    reload = PathReload(
        iter_paths=lambda: (str(path) for path in content.iter_content_paths()),
        on_reload=[content.load_content, notify_reload],
    )

    on_startup += [reload.startup]
    on_shutdown += [reload.shutdown]
