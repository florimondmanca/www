from .. import settings
from . import content
from .reload import hotreload

on_startup = [content.load_content]
on_shutdown = []

if settings.DEBUG:
    on_startup += [hotreload.startup]
    on_shutdown += [hotreload.shutdown]
