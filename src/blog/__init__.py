from .app import app
from .events import on_startup
from .resources import static

__all__ = ["app", "static", "on_startup"]
