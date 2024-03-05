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

        context = {
            "build_reports": build_reports,
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

        context = {
            "build_report": build_report,
        }

        if request.query_params.get("photos") == "true":
            context["photos_html"] = templates.env.get_template(
                "views/build_reports/_detail_photos.jinja"
            ).render(context)

        return templates.TemplateResponse(
            request, "views/build_reports/detail.jinja", context
        )
