from .. import content, settings
from .reload import hotreload

on_startup = [content.load_content]
on_shutdown = []

if settings.DEBUG:  # pragma: no cover
    on_startup += [hotreload.startup]
    on_shutdown += [hotreload.shutdown]
