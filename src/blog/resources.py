import contextvars

import markdown as md
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings
from .models import Index

index = Index()
templates = Jinja2Templates(directory=str(settings.BLOG_ROOT / "templates"))
static = StaticFiles(directory=str(settings.BLOG_ROOT / "static"))
sass = StaticFiles(directory=str(settings.BLOG_ROOT / "sass"))
markdown = md.Markdown(extensions=settings.BLOG_MARKDOWN_EXTENSIONS)

CTX_VAR_REQUEST: contextvars.ContextVar[Request] = contextvars.ContextVar("request")


def with_base(path: str) -> str:
    if path.startswith(("http://", "https://")):
        # 'path' is a full-fledged URL, probably to an external resource.
        return path

    # NOTE: we use a ContextVar instead of turning this into an
    # '@jinja2.contextfunction' because the request may not be available
    # in the current jinja2 context (i.e. it may be in a parent context).
    # A ContextVar can be accessed regardless of where 'with_base()' is called.
    request = CTX_VAR_REQUEST.get()
    root_path = request.get("root_path", "")
    return f"{root_path}{path}"


templates.env.globals["with_base"] = with_base
templates.env.globals["GA_ID"] = settings.BLOG_GA_ID
