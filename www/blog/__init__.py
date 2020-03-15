from .. import settings
from ..resources import broadcast
from . import content
from .reloader import ContentReloader
from .routes import routes

on_startup = [content.load_content]
on_shutdown = []

if settings.DEBUG:

    async def notify_reload() -> None:
        await broadcast.publish(channel=settings.BLOG_RELOAD_CHANNEL, message="")

    reloader = ContentReloader(on_reload=[content.load_content, notify_reload])
    on_startup += [reloader.start]
    on_shutdown += [reloader.stop]

__all__ = ["on_startup", "on_shutdown", "routes"]
