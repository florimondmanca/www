from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from .. import settings
from ..di import resolve
from ..domain.repositories import (
    BlogPostingRepository,
    CategoryRepository,
    KeywordRepository,
)
from .templating import Templates


async def _get_base_context(request: Request) -> dict:
    category_repository = resolve(CategoryRepository)
    context: dict = {"request": request}
    context["categories"] = await category_repository.find_all()
    return context


class _ContextMixin:
    async def get_context(self, request: Request) -> dict:
        return await _get_base_context(request)


class TemplateView(_ContextMixin):
    template_name: str
    status_code: int = 200

    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)
        context = await self.get_context(request)
        return templates.TemplateResponse(
            self.template_name, context, status_code=self.status_code
        )


class Home(TemplateView, HTTPEndpoint):
    template_name = "views/home.jinja"

    async def get_context(self, request: Request) -> dict:
        blog_posting_repository = resolve(BlogPostingRepository)

        context = await super().get_context(request)
        context["blog_postings"] = await blog_posting_repository.find_all()

        return context


async def posts(request: Request) -> Response:
    templates = resolve(Templates)
    context = {"request": request, **_common_context()}
    return templates.TemplateResponse("views/posts.jinja", context=context)


async def legacy_blog_home(request: Request) -> Response:
    return RedirectResponse(request.url_for("home"))


class BlogPostingDetail(TemplateView, HTTPEndpoint):
    template_name = "views/blog_posting_detail.jinja"

    async def get_context(self, request: Request) -> dict:
        blog_posting_repository = resolve(BlogPostingRepository)

        context = await super().get_context(request)

        slug = request.path_params["slug"]
        blog_posting = await blog_posting_repository.find_by_slug(slug)

        if blog_posting is None:
            raise HTTPException(404)

        context["blog_posting"] = blog_posting

        return context


class CategoryDetail(TemplateView, HTTPEndpoint):
    template_name = "views/category_detail.jinja"

    async def get_context(self, request: Request) -> dict:
        category_repository = resolve(CategoryRepository)
        blog_posting_repository = resolve(BlogPostingRepository)

        context = await super().get_context(request)

        slug = request.path_params["slug"]
        category = await category_repository.find_by_slug(slug)

        if category is None:
            raise HTTPException(404)

        context["category"] = category
        context["blog_postings"] = await blog_posting_repository.find_all_by_category(
            category
        )

        return context


class KeywordDetail(TemplateView, HTTPEndpoint):
    template_name = "views/keyword_detail.jinja"

    async def get_context(self, request: Request) -> dict:
        keyword_repository = resolve(KeywordRepository)
        blog_posting_repository = resolve(BlogPostingRepository)

        context = await super().get_context(request)

        name = request.path_params["name"]
        keyword = await keyword_repository.find_by_name(name)

        if keyword is None:
            raise HTTPException(404)

        context["keyword"] = keyword
        context["blog_postings"] = await blog_posting_repository.find_all_by_keyword(
            keyword
        )

        return context


async def not_found(request: Request, exc: Exception) -> Response:
    templates = resolve(Templates)
    context = await _get_base_context(request)
    return templates.TemplateResponse("views/404.jinja", context, status_code=404)


async def internal_server_error(request: Request, exc: Exception) -> Response:
    templates = resolve(Templates)
    context = await _get_base_context(request)
    return templates.TemplateResponse("views/500.jinja", context, status_code=500)


async def error(request: Request) -> Response:
    if settings.TESTING:
        raise RuntimeError("Example server error")
    return RedirectResponse("/")  # pragma: no cover
