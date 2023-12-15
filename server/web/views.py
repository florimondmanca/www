from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from server.web.params import get_page_param

from .. import settings
from ..di import resolve
from ..domain.repositories import (
    CategoryRepository,
    KeywordRepository,
    PostFilterSet,
    PostRepository,
)
from .context import get_navbar_context
from .templating import Templates


class Home(HTTPEndpoint):
    template_name = "views/index.jinja"

    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)
        post_repository = resolve(PostRepository)

        page = get_page_param(request)
        pagination = await post_repository.find_all(PostFilterSet(page=page))

        context = await get_navbar_context()
        context["pagination"] = pagination

        if request.headers.get("HX-Request"):
            template_name = "partials/post_list.jinja"
        else:
            template_name = "views/index.jinja"

        return templates.TemplateResponse(request, template_name, context)


async def legacy_blog_home(request: Request) -> Response:
    return RedirectResponse(request.url_for("home"))


class PostDetail(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)
        post_repository = resolve(PostRepository)

        slug = request.path_params["slug"]
        post = await post_repository.find_by_slug(slug)

        if post is None:
            raise HTTPException(404)

        context = await get_navbar_context()
        context["post"] = post

        template_name = "views/post/detail.jinja"

        return templates.TemplateResponse(request, template_name, context)


class CategoryDetail(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)
        category_repository = resolve(CategoryRepository)
        post_repository = resolve(PostRepository)

        slug = request.path_params["slug"]
        category = await category_repository.find_by_slug(slug)

        if category is None:
            raise HTTPException(404)

        page = get_page_param(request)

        context = await get_navbar_context()
        context["category"] = category
        context["pagination"] = await post_repository.find_all(
            PostFilterSet(page=page, category=category)
        )

        if request.headers.get("HX-Request"):
            template_name = "partials/post_list.jinja"
        else:
            template_name = "views/category/detail.jinja"

        return templates.TemplateResponse(request, template_name, context)


class KeywordDetail(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)
        keyword_repository = resolve(KeywordRepository)
        post_repository = resolve(PostRepository)

        name = request.path_params["name"]
        keyword = await keyword_repository.find_by_name(name)

        if keyword is None:
            raise HTTPException(404)

        context = await get_navbar_context()
        context["keyword"] = keyword
        context["pagination"] = await post_repository.find_all(
            PostFilterSet(page=get_page_param(request), keyword=keyword)
        )

        if request.headers.get("HX-Request"):
            template_name = "partials/post_list.jinja"
        else:
            template_name = "views/tag/detail.jinja"

        return templates.TemplateResponse(request, template_name, context)


async def not_found(request: Request, _: Exception) -> Response:
    templates = resolve(Templates)
    context = await get_navbar_context()
    return templates.TemplateResponse(
        request, "views/404.jinja", context, status_code=404
    )


async def internal_server_error(request: Request, _: Exception) -> Response:
    templates = resolve(Templates)
    context = await get_navbar_context()
    return templates.TemplateResponse(
        request, "views/500.jinja", context, status_code=500
    )


async def error(_: Request) -> Response:
    if settings.TESTING:
        raise RuntimeError("Example server error")

    return RedirectResponse("/")  # pragma: no cover
