import contextvars

import broadcaster
import datadog
import ddtrace
from ddtrace.filters import FilterRequestsOnUrl
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings
from .blog.reload import hotreload
from .monitoring import FilterDropIf, FilterRedirectResponses

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
static = StaticFiles(directory=str(settings.STATIC_DIR))
sass = StaticFiles(directory=str(settings.SASS_DIR))

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
templates.env.globals["settings"] = settings
templates.env.globals["hotreload"] = hotreload

broadcast = broadcaster.Broadcast("memory://")

tracer = ddtrace.Tracer()
trace_filters = [
    FilterRedirectResponses(),
    FilterRequestsOnUrl(settings.DD_TRACE_FILTER_URLS),
    FilterDropIf(lambda: settings.TESTING),
]

statsd = datadog.DogStatsd(
    host="dummy" if settings.TESTING else settings.DD_AGENT_HOST,
    port=8125,
    constant_tags=settings.DD_TAGS,
)
