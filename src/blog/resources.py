from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings
from .models import Index

index = Index(root=settings.CONTENT_ROOT)
templates = Jinja2Templates(directory=str(settings.ROOT / "templates"))
static = StaticFiles(directory=str(settings.ROOT / "static"))
sass = StaticFiles(directory=str(settings.ROOT / "sass"))


def with_base(*paths: str, request: Request = None) -> str:
    if request is None:
        request = templates.env.globals.get("request")
    assert request is not None
    root_path = request.get("root_path", "")
    return f"{root_path}{''.join(paths)}"


templates.env.globals["with_base"] = with_base
