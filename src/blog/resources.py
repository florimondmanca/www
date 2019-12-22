from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings
from .models import Index

index = Index(root=settings.CONTENT_ROOT)
templates = Jinja2Templates(directory=str(settings.ROOT / "templates"))
static = StaticFiles(directory=str(settings.ROOT / "static"))


def with_base(*paths: str, request: Request) -> str:
    root_path = request.get("root_path", "")
    return f"{root_path}{''.join(paths)}"


templates.env.globals["with_base"] = with_base
