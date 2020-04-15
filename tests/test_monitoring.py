from typing import Any, List

import httpx
import pytest
from ddtrace import Span
from ddtrace.ext import http

from www import resources, settings


@pytest.fixture()
def patch_disable_testing(monkeypatch: Any) -> None:
    monkeypatch.setattr(settings, "TESTING", False)


def is_dropped(span: Span) -> bool:
    for filtr in resources.trace_filters:
        trace = filtr.process_trace([span])
        if trace is None:
            return True
    return False


@pytest.mark.usefixtures("patch_disable_testing")
@pytest.mark.parametrize(
    "url, dropped",
    [
        ("http://localhost:8000", False),
        ("http://florimond.dev", False),
        ("http://florimond.dev/", False),
        ("https://florimond.dev", False),
        ("http://localhost:8000/feed.rss", True),
        ("http://florimond.dev/robots.txt", True),
        ("https://florimond.dev/favicon.ico", True),
        ("http://localhost:8000/blog/", False),
        ("http://florimond.dev/static/picture.png", True),
    ],
)
def test_trace_filter_urls(url: str, dropped: bool) -> None:
    span = Span(resources.tracer, name="test")
    span.set_tag(http.URL, url)
    assert is_dropped(span) is dropped


@pytest.mark.usefixtures("patch_disable_testing")
@pytest.mark.parametrize(
    "status_code, dropped",
    [(200, False), (299, False), (300, True), (399, True), (400, False)],
)
def test_trace_filter_redirect_responses(status_code: int, dropped: bool) -> None:
    span = Span(resources.tracer, name="test")
    span.set_tag(http.STATUS_CODE, status_code)
    assert is_dropped(span) is dropped


def test_trace_filter_testing() -> None:
    span = Span(resources.tracer, name="test")
    assert is_dropped(span)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "headers, domain",
    [
        ({}, "unknown"),
        ({"host": "florimond.dev"}, "florimond.dev"),
        ({"host": "blog.florimond.dev"}, "blog.florimond.dev"),
        ({"host": "florimondmanca.com"}, "florimondmanca.com"),
        ({"host": "blog.florimondmanca.com"}, "blog.florimondmanca.com"),
        ({"host": "example.com"}, "unknown"),
    ],
)
async def test_metrics(
    client: httpx.AsyncClient, monkeypatch: Any, headers: dict, domain: str,
) -> None:
    packets: List[str] = []
    monkeypatch.setattr(resources.statsd, "_send", packets.append)

    r = await client.get("https://testserver/", allow_redirects=False, headers=headers)
    assert r.status_code in (200, 301)

    assert len(packets) == 1
    packet = packets[0]
    metric, typ, tagdef = packet.split("|")
    assert metric == "www.hits:1"
    assert typ == "c"
    tags = tagdef.lstrip("#").split(",")
    assert f"domain:{domain}" in tags
    assert f"status_code:{r.status_code}" in tags


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url",
    [
        "http://testserver/feed.rss",
        "http://testserver/robots.txt/",
        "http://testserver/static/img.png",
        "http://testserver/static/fonts/roboto.ttf",
    ],
)
async def test_metrics_filter_static(
    client: httpx.AsyncClient, monkeypatch: Any, url: str,
) -> None:
    packets: List[str] = []
    monkeypatch.setattr(resources.statsd, "_send", packets.append)
    r = await client.get(url, allow_redirects=False)
    assert r.status_code in (200, 307, 404)
    assert not packets
