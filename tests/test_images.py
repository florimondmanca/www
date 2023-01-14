import re

import httpx
import pytest

from server import settings
from server.di import resolve
from server.domain.repositories import BlogPostingRepository
from server.tools import imgoptimize, imgsize

IMAGE_RE = re.compile(r"\!\[[^\[\]]*\]\((?P<url>[^\[\]]*?)\)")


@pytest.mark.asyncio
async def test_images(client: httpx.AsyncClient) -> None:
    """
    All images linked in articles must exist and be local files.
    """
    blog_posting_repository = resolve(BlogPostingRepository)

    remote_urls = []
    for blog_posting in (await blog_posting_repository.find_all()).items:
        url = image.content_url if (image := blog_posting.image) is not None else None

        if url is not None and url.startswith("http"):
            remote_urls.append(url)

        url = blog_posting.thumbnail_url
        if url is not None and url.startswith("http"):
            remote_urls.append(url)

        urls = IMAGE_RE.findall(blog_posting.text)
        for url in urls:
            assert url is not None
            response = await client.get(url)
            if response.status_code == 404:
                # Image URL not found on local server -- it's probably remote.
                remote_urls.append(url)
            filesize_kb = len(response.content) / 10254
            assert filesize_kb < settings.IMAGE_ALLOWED_MAX_SIZE_KB, url

    if remote_urls:
        raise AssertionError(remote_urls)


def test_imgsize() -> None:
    assert imgsize.main() == 0


def test_imgoptimize() -> None:
    assert imgoptimize.main(check=True) == 0
