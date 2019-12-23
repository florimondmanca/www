import contextvars

from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings
from .models import Index

index = Index(root=settings.CONTENT_ROOT)
templates = Jinja2Templates(directory=str(settings.ROOT / "templates"))
static = StaticFiles(directory=str(settings.ROOT / "static"))
sass = StaticFiles(directory=str(settings.ROOT / "sass"))

CTX_VAR_REQUEST: contextvars.ContextVar[Request] = contextvars.ContextVar("request")


def with_base(*paths: str) -> str:
    # NOTE: we use a ContextVar instead of turning this into an
    # '@jinja2.contextfunction' because the request may not be available
    # in the current jinja2 context (i.e. it may be in a parent context).
    # A ContextVar can be accessed regardless of where 'with_base()' is called.
    request = CTX_VAR_REQUEST.get()
    root_path = request.get("root_path", "")
    return f"{root_path}{''.join(paths)}"


templates.env.globals["with_base"] = with_base
