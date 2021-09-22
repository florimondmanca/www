"""
Tests relative to the ecodesign of the application.

Based on best practices from GreenIT-Analysis.
"""

import httpx
import pytest


@pytest.mark.asyncio
async def test_resources_compressed(client: httpx.AsyncClient) -> None:
    url = "http://florimond.dev/"
    headers = {"Accept-Encoding": "gzip, deflate"}
    resp = await client.get(url, headers=headers, allow_redirects=False)
    assert resp.status_code == 200
    assert resp.headers["Content-Encoding"] == "gzip"
