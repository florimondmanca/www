from .. import resources, settings
from . import content
from .reloader import ContentReloader

on_startup = [content.load_content]
on_shutdown = []

if settings.DEBUG:

    async def notify_reload() -> None:
        channel = settings.BLOG_RELOAD_CHANNEL
        message = "reload"
        await resources.broadcast.publish(channel, message)

    reloader = ContentReloader(on_reload=[content.load_content, notify_reload])
    on_startup += [reloader.start]
    on_shutdown += [reloader.stop]
