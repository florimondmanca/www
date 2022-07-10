from .. import settings
from ..domain.entities import Page
from .urls import to_production_url


def build_meta_tags(page: Page) -> list[dict]:
    path = page.permalink + ("" if page.permalink.endswith("/") else "/")
    url = to_production_url(path)

    image_url = page.metadata.image
    if image_url:
        image_url = to_production_url(image_url)

    meta_tags: list[dict[str, str | None]] = [
        # General
        dict(name="description", content=page.metadata.description),
        dict(name="image", content=image_url),
        dict(itemprop="name", content=page.metadata.title),
        dict(itemprop="description", content=page.metadata.description),
        # Twitter
        dict(name="twitter:url", content=url),
        dict(name="twitter:title", content=page.metadata.title),
        dict(name="twitter:description", content=page.metadata.description),
        dict(name="twitter:image", content=image_url),
        dict(name="twitter:card", content="summary_large_image"),
        dict(name="twitter:site", content="@florimondmanca"),
        # OpenGraph
        dict(property="og:url", content=url),
        dict(property="og:type", content="article"),
        dict(property="og:title", content=page.metadata.title),
        dict(property="og:description", content=page.metadata.description),
        dict(property="og:image", content=image_url),
        dict(property="og:site_name", content=settings.SITE_TITLE),
        dict(property="article:published_time", content=page.metadata.date),
    ]

    for tag in page.metadata.tags:
        meta_tags.append(dict(property="article:tag", content=tag.slug))

    meta_tags = [attrs for attrs in meta_tags if attrs["content"] is not None]

    return meta_tags
