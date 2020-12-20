import re

import httpx
import pytest

from server.resources import index

IMAGE_RE = re.compile(r"\!\[[^\[\]]*\]\((?P<url>[^\[\]]*?)\)")


@pytest.mark.asyncio
async def test_images(client: httpx.AsyncClient) -> None:
    """
    All images linked in articles must exist and be local files.
    """
    remote_urls = []
    for page in index.pages:
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

    if remote_urls:
        raise AssertionError(remote_urls)
