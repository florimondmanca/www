from .app import app
from .events import on_shutdown, on_startup
from .resources import static

__all__ = ["app", "static", "on_shutdown", "on_startup"]
