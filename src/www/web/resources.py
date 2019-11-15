from starlette.templating import Jinja2Templates

from . import settings

templates = Jinja2Templates(directory=str(settings.DIR / "templates"))
templates.env.globals["blog_url"] = settings.BLOG_URL
