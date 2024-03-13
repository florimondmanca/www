from starlette.routing import BaseRoute, Host, Mount, Route, Router, WebSocketRoute

from .. import settings
from ..di import resolve
from . import views
from .reload import HotReload
from .statics import CachedStaticFiles


def get_routes() -> list[BaseRoute]:
    static = CachedStaticFiles(
        directory=str(settings.STATIC_DIR),
        max_age=7 * 86400,  # 7 days
    )

    hotreload = resolve(HotReload)

    routes = [
        Mount(settings.STATIC_ROOT, static, name="static"),
        # These files need to be exposed at the root, not '/static/'.
        Route("/favicon.ico", static, name="favicon"),
        Route("/robots.txt", static, name="robots"),
        Route("/", views.Home, name="home"),
        Route(
            "/build-reports",
            views.BuildReportList,
            name="build_reports",
        ),
        Route(
            "/build-reports/{slug:str}",
            views.BuildReportDetail,
            name="build_reports:detail",
        ),
        Route(
            "/build-reports/categories/{category:str}",
            views.BuildReportCategoryDetail,
            name="build_reports:categories:detail",
        ),
    ]

    if settings.DEBUG:  # pragma: no cover
        routes += [WebSocketRoute("/hot-reload", hotreload, name="hot-reload")]

    return routes
