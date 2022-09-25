from pathlib import Path
from typing import Any

import frontmatter
import markdown as md

from .. import settings
from ..application.parsers import Parser
from ..di import resolve
from ..domain.entities import Metadata, Tag
from ..domain.repositories import CategoryRepository


class MarkdownParser(Parser):
    def __init__(self) -> None:
        self._impl = md.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)

    def parse(self, raw: str) -> tuple[str, Metadata]:
        category_repository = resolve(CategoryRepository)

        post = frontmatter.loads(raw)
        content = self._impl.reset().convert(post.content)
        attrs = dict(post)
        image, image_thumbnail = _process_image(attrs)
        category = (
            category_repository.find_by_name(category_name)
            if (category_name := attrs.get("category")) is not None
            else None
        )

        metadata = Metadata(
            title=attrs.get("title", ""),
            description=attrs.get("description"),
            category=category,
            date=attrs.get("date"),
            image=image,
            image_thumbnail=image_thumbnail,
            image_caption=attrs.get("image_caption"),
            tags=[Tag(slug) for slug in attrs.get("tags", [])],
        )

        return content, metadata


def _process_image(attrs: dict[str, Any]) -> tuple[str | None, str | None]:
    image = attrs.get("image")
    image_thumbnail = attrs.get("image_thumbnail")

    is_image_self_hosted = isinstance(image, str) and image.startswith(
        settings.STATIC_ROOT
    )

    if image_thumbnail is None and is_image_self_hosted:
        # By default, use the same image
        image_thumbnail = image

    if image_thumbnail == "__auto__":
        # Convention: '/static/example.jpg' -> '/static/example_thumbnail.jpg'
        if is_image_self_hosted:
            assert isinstance(image, str)
            image_thumbnail = _append_filename(image, "_thumbnail")
        else:
            image_thumbnail = None

    assert image is None or isinstance(image, str)
    assert image_thumbnail is None or isinstance(image_thumbnail, str)

    return image, image_thumbnail


def _append_filename(filename: str, suffix: str) -> str:
    path = Path(filename)
    name = f"{path.stem}{suffix}{path.suffix}"
    return str(path.with_name(name))
