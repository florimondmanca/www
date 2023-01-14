from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from .. import settings
from ..di import resolve
from ..domain.entities import Page
from ..domain.repositories import (
    BlogPostingFilterSet,
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

    def get_template_name(self, request: Request) -> str:
        return self.template_name

    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)
        context = await self.get_context(request)
        template_name = self.get_template_name(request)
        return templates.TemplateResponse(
            template_name, context, status_code=self.status_code
        )


class BlogPostingPageView(TemplateView):
    def get_template_name(self, request: Request) -> str:
        if request.headers.get("HX-Request"):
            return "partials/blog_posting_list.jinja"
        return super().get_template_name(request)

    def get_page(self, request: Request) -> Page:
        try:
            page_number = int(request.query_params["page"])
        except (ValueError, TypeError, KeyError):
            page_number = 1

        return Page(number=page_number, size=9)


class Home(BlogPostingPageView, HTTPEndpoint):
    template_name = "views/home.jinja"

    async def get_context(self, request: Request) -> dict:
        blog_posting_repository = resolve(BlogPostingRepository)

        context = await super().get_context(request)

        context["pagination"] = await blog_posting_repository.find_all(
            BlogPostingFilterSet(page=self.get_page(request))
        )

        return context


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


class CategoryDetail(BlogPostingPageView, HTTPEndpoint):
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
        context["pagination"] = await blog_posting_repository.find_all(
            BlogPostingFilterSet(page=self.get_page(request), category=category)
        )

        return context


class KeywordDetail(BlogPostingPageView, HTTPEndpoint):
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
        context["pagination"] = await blog_posting_repository.find_all(
            BlogPostingFilterSet(page=self.get_page(request), keyword=keyword)
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
