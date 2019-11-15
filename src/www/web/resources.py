import typing

import jinja2
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings

templates = Jinja2Templates(directory=str(settings.DIR / "templates"))


@jinja2.contextfunction
def relative_url_for(context: dict, name: str, **path_params: typing.Any) -> str:
    request = context["request"]
    router = request["router"]
    url_path = router.url_path_for(name, **path_params)
    return str(url_path)


templates.env.globals["relative_url_for"] = relative_url_for
templates.env.globals["blog_url"] = settings.BLOG_URL

static_files = StaticFiles(directory=str(settings.DIR / "static"))
