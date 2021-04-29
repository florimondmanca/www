import re

import httpx
import pytest

from server import settings
from server.resources import index
from server.tools import imgoptimize, imgsize

IMAGE_RE = re.compile(r"\!\[[^\[\]]*\]\((?P<url>[^\[\]]*?)\)")


@pytest.mark.asyncio
async def test_images(client: httpx.AsyncClient) -> None:
    """
    All images linked in articles must exist and be local files.
    """
    remote_urls = []
    for page in index.get_pages():
        url = page.frontmatter.image
        if url is not None and url.startswith("http"):
            remote_urls.append(url)

        url = page.frontmatter.image_thumbnail
        if url is not None and url.startswith("http"):
            remote_urls.append(url)

        urls = IMAGE_RE.findall(page.content)
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
