import datetime as dt

import datadog
import ddtrace
from ddtrace.filters import FilterRequestsOnUrl
from starlette.exceptions import HTTPException
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings
from .blog.reload import hotreload
from .monitoring import FilterDropIf, FilterRedirectResponses

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
static = StaticFiles(directory=str(settings.STATIC_DIR))
sass = StaticFiles(directory=str(settings.SASS_DIR))


def raise_server_error(message: str) -> None:
    raise HTTPException(500, detail=message)


templates.env.globals["now"] = dt.datetime.now
templates.env.globals["raise"] = raise_server_error
templates.env.globals["settings"] = settings
templates.env.globals["hotreload"] = hotreload

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
