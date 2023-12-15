from starlette.requests import Request

from ..domain.entities import Page


def get_page_param(request: Request) -> Page:
    try:
        page_number = int(request.query_params["page"])
    except (ValueError, TypeError, KeyError):
        page_number = 1

    return Page(number=page_number, size=9)
