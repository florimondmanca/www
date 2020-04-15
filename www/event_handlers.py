from . import content, monitoring, settings
from .reload import hotreload

on_startup = [content.load_content, monitoring.on_startup]
on_shutdown = []

if settings.DEBUG:
    on_startup += [hotreload.startup]
    on_shutdown += [hotreload.shutdown]
