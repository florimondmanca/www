from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response

from .. import settings
from ..di import resolve
from ..domain.repositories import BuildReportRepository
from .templating import Templates


class Home(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)

        return templates.TemplateResponse(request, "views/index.jinja")


class BuildReportList(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)
        build_report_repository = resolve(BuildReportRepository)

        build_reports = await build_report_repository.find_all()
        categories = sorted(await build_report_repository.get_unique_categories())

        context = {
            "build_reports": build_reports,
            "categories": categories,
        }

        return templates.TemplateResponse(
            request, "views/build_reports/list.jinja", context
        )


class BuildReportDetail(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)
        build_report_repository = resolve(BuildReportRepository)

        slug = request.path_params["slug"]

        build_report = await build_report_repository.find_one(slug=slug)

        context: dict = {
            "build_report": build_report,
            "show_photos": request.query_params.get("photos") == "true",
        }

        return templates.TemplateResponse(
            request, "views/build_reports/detail.jinja", context
        )


class BuildReportCategoryDetail(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        templates = resolve(Templates)
        build_report_repository = resolve(BuildReportRepository)

        category = request.path_params["category"]

        build_reports = await build_report_repository.find_all(category=category)
        categories = sorted(await build_report_repository.get_unique_categories())

        context = {
            "category": category,
            "build_reports": build_reports,
            "categories": categories,
            "current_category": category,
        }

        return templates.TemplateResponse(
            request, "views/build_reports/categories/detail.jinja", context
        )
