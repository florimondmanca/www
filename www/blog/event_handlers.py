from . import content

on_startup = [content.load_content]
on_shutdown = []  # type: ignore
