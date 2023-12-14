from .. import settings
from ..domain.entities import ObjWithMeta
from .urls import get_absolute_url, to_production_url


def build_meta_tags(obj: ObjWithMeta) -> list[dict]:
    url = to_production_url(get_absolute_url(obj))
    title = obj.meta_title
    description = obj.meta_description
    image_url = obj.meta_image_url
    date_published = obj.meta_date_published
    keywords = obj.meta_keywords

    if image_url is not None:
        image_url = to_production_url(image_url)

    meta_tags: list[dict[str, str | None]] = [
        # General
        dict(name="description", content=description),
        dict(name="image", content=image_url),
        dict(itemprop="name", content=title),
        dict(itemprop="description", content=description),
        # OpenGraph
        dict(property="og:url", content=url),
        dict(property="og:type", content="article"),
        dict(property="og:title", content=title),
        dict(property="og:description", content=description),
        dict(property="og:image", content=image_url),
        dict(property="og:site_name", content=settings.SITE_TITLE),
        dict(
            property="article:published_time",
            content=date_published.strftime("%Y-%M-%d")
            if date_published is not None
            else None,
        ),
    ]

    for keyword in keywords:
        meta_tags.append(dict(property="article:tag", content=keyword))

    meta_tags = [attrs for attrs in meta_tags if attrs["content"] is not None]

    return meta_tags
