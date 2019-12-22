from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from .exceptions import DoesNotExist
from .resources import index, templates


async def home(request: Request) -> Response:
    articles = index.find_all(order="desc")

    template = "index.jinja"
    context = {"request": request, "articles": articles}

    return templates.TemplateResponse(template, context=context)


async def article_detail(request: Request) -> Response:
    slug = request.path_params["slug"]

    try:
        article = index.find_one_or_error(lambda article: article.slug == slug)
    except DoesNotExist:
        raise HTTPException(404)

    template = "article.jinja"
    context = {"request": request, "article": article}

    return templates.TemplateResponse(template, context=context)


async def tag_detail(request: Request) -> Response:
    tag = request.path_params["tag"]
    articles = index.find_all(lambda article: tag in article.frontmatter.tags)

    template = "index.jinja"
    context = {"request": request, "articles": articles}
    return templates.TemplateResponse(template, context=context)
