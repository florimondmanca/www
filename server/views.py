from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from . import resources, settings


def _common_context() -> dict:
    return {
        "get_post_pages": resources.index.get_post_pages,
        "get_category_pages": resources.index.get_category_pages,
    }


async def home(request: Request) -> Response:
    context = {"request": request, **_common_context()}
    return resources.templates.TemplateResponse("views/home.jinja", context=context)


async def legacy_blog_home(request: Request) -> Response:
    return RedirectResponse(request.url_for("home"))


class RenderPage(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        permalink = "/" + request.path_params["permalink"]

        for page in resources.index.get_pages():
            if page.permalink == permalink:
                break
        else:
            raise HTTPException(404)

        context = {"request": request, "page": page, **_common_context()}

        return resources.templates.TemplateResponse("views/page.jinja", context=context)


async def not_found(request: Request, exc: Exception) -> Response:
    context = {"request": request, **_common_context()}
    return resources.templates.TemplateResponse(
        "views/404.jinja", context=context, status_code=404
    )


async def internal_server_error(request: Request, exc: Exception) -> Response:
    context = {"request": request, **_common_context()}
    return resources.templates.TemplateResponse(
        "views/500.jinja", context=context, status_code=500
    )


async def error(request: Request) -> Response:
    if settings.TESTING:
        raise RuntimeError("Example server error")
    return RedirectResponse("/")  # pragma: no cover
