from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from . import resources, settings


async def home(request: Request) -> Response:
    context = {
        "request": request,
        "get_articles": resources.index.articles_by_date,
    }
    return resources.templates.TemplateResponse("views/home.jinja", context=context)


async def legacy_blog_home(request: Request) -> Response:
    return RedirectResponse(request.url_for("home"))


class RenderPage(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        permalink = "/" + request.path_params["permalink"]

        for page in resources.index.pages:
            if page.permalink == permalink:
                break
        else:
            raise HTTPException(404)

        context = {
            "request": request,
            "page": page,
            "get_articles": resources.index.articles_by_date,
        }

        return resources.templates.TemplateResponse("views/page.jinja", context=context)


async def not_found(request: Request, exc: Exception) -> Response:
    return resources.templates.TemplateResponse(
        "views/404.jinja", context={"request": request}, status_code=404
    )


async def internal_server_error(request: Request, exc: Exception) -> Response:
    return resources.templates.TemplateResponse(
        "views/500.jinja", context={"request": request}, status_code=500
    )


async def error(request: Request) -> Response:
    if settings.TESTING:
        raise RuntimeError("Example server error")
    return RedirectResponse("/")  # pragma: no cover
