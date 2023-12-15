from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from .. import settings
from ..di import resolve
from ..domain.entities import Page
from ..domain.repositories import (
    PostFilterSet,
    PostRepository,
    CategoryRepository,
    KeywordRepository,
)
from .templating import Templates


async def _get_base_context() -> dict:
    category_repository = resolve(CategoryRepository)

    return {
        "categories": await category_repository.find_all(),
    }


class _ContextMixin:
    async def get_context(self, _: Request) -> dict:
        return await _get_base_context()


class TemplateView(_ContextMixin):
    template_name: str
    status_code: int = 200

    def get_template_name(self, _: Request) -> str:
        return self.template_name

    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)
        context = await self.get_context(request)
        template_name = self.get_template_name(request)
        return templates.TemplateResponse(
            request, template_name, context, status_code=self.status_code
        )


class PostPageView(TemplateView):
    def get_template_name(self, request: Request) -> str:
        if request.headers.get("HX-Request"):
            return "partials/post_list.jinja"
        return super().get_template_name(request)

    def get_page(self, request: Request) -> Page:
        try:
            page_number = int(request.query_params["page"])
        except (ValueError, TypeError, KeyError):
            page_number = 1

        return Page(number=page_number, size=9)


class Home(PostPageView, HTTPEndpoint):
    template_name = "views/home.jinja"

    async def get_context(self, request: Request) -> dict:
        post_repository = resolve(PostRepository)

        context = await super().get_context(request)

        context["pagination"] = await post_repository.find_all(
            PostFilterSet(page=self.get_page(request))
        )

        return context


async def legacy_blog_home(request: Request) -> Response:
    return RedirectResponse(request.url_for("home"))


class PostDetail(TemplateView, HTTPEndpoint):
    template_name = "views/post/detail.jinja"

    async def get_context(self, request: Request) -> dict:
        post_repository = resolve(PostRepository)

        context = await super().get_context(request)

        slug = request.path_params["slug"]
        post = await post_repository.find_by_slug(slug)

        if post is None:
            raise HTTPException(404)

        context["post"] = post

        return context


class CategoryDetail(PostPageView, HTTPEndpoint):
    template_name = "views/category/detail.jinja"

    async def get_context(self, request: Request) -> dict:
        category_repository = resolve(CategoryRepository)
        post_repository = resolve(PostRepository)

        context = await super().get_context(request)

        slug = request.path_params["slug"]
        category = await category_repository.find_by_slug(slug)

        if category is None:
            raise HTTPException(404)

        context["category"] = category
        context["pagination"] = await post_repository.find_all(
            PostFilterSet(page=self.get_page(request), category=category)
        )

        return context


class KeywordDetail(PostPageView, HTTPEndpoint):
    template_name = "views/tag/detail.jinja"

    async def get_context(self, request: Request) -> dict:
        keyword_repository = resolve(KeywordRepository)
        post_repository = resolve(PostRepository)

        context = await super().get_context(request)

        name = request.path_params["name"]
        keyword = await keyword_repository.find_by_name(name)

        if keyword is None:
            raise HTTPException(404)

        context["keyword"] = keyword
        context["pagination"] = await post_repository.find_all(
            PostFilterSet(page=self.get_page(request), keyword=keyword)
        )

        return context


async def not_found(request: Request, _: Exception) -> Response:
    templates = resolve(Templates)
    context = await _get_base_context()
    return templates.TemplateResponse(
        request, "views/404.jinja", context, status_code=404
    )


async def internal_server_error(request: Request, _: Exception) -> Response:
    templates = resolve(Templates)
    context = await _get_base_context()
    return templates.TemplateResponse(
        request, "views/500.jinja", context, status_code=500
    )


async def error(_: Request) -> Response:
    if settings.TESTING:
        raise RuntimeError("Example server error")

    return RedirectResponse("/")  # pragma: no cover
