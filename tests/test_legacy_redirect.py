import typing

import pytest

from .utils import TestClient

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "start_url, urls",
    [
        pytest.param(
            "http://florimondmanca.com", [("http://florimond.dev/", 301)], id="home",
        ),
        pytest.param(
            "http://blog.florimondmanca.com",
            [("http://blog.florimond.dev/", 301), ("http://florimond.dev/blog/", 301)],
            id="blog:home",
        ),
        pytest.param(
            "http://blog.florimondmanca.com/let-the-journey-begin",
            [
                ("http://blog.florimond.dev/let-the-journey-begin", 301),
                ("http://florimond.dev/blog/let-the-journey-begin", 301),
                (
                    "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin",
                    301,
                ),
                (
                    "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin/",
                    307,
                ),
            ],
            id="blog:article",
        ),
    ],
)
async def test_legacy_redirect_chains(
    client: TestClient, start_url: str, urls: typing.List[str]
) -> None:
    resp = await client.get(start_url, allow_redirects=True)
    assert resp.status_code == 200
    assert [(r.headers["Location"], r.status_code) for r in resp.history] == urls


@pytest.mark.parametrize(
    "blog_dot_dev_path, dot_dev_path",
    [
        ("/let-the-journey-begin", "/articles/2018/07/let-the-journey-begin/"),
        (
            "/a-practical-usage-of-chainmap-in-python",
            "/articles/2018/07/a-practical-usage-of-chainmap-in-python/",
        ),
        (
            "/cheap-and-easy-deployment-captainduckduck-1",
            "/articles/2018/07/cheap-and-easy-deployment-captainduckduck-1/",
        ),
        (
            "/why-i-started-using-python-type-annotations-and-why-you-should-too",
            (
                "/articles/2018/07"
                "/why-i-started-using-python-type-annotations-and-why-you-should-too/"
            ),
        ),
        (
            "/cheap-and-easy-deployment-captainduckduck-2",
            "/articles/2018/08/cheap-and-easy-deployment-captainduckduck-2/",
        ),
        (
            "/python-mutable-defaults-are-the-source-of-all-evil",
            "/articles/2018/08/python-mutable-defaults-are-the-source-of-all-evil/",
        ),
        (
            "/restful-api-design-13-best-practices-to-make-your-users-happy",
            (
                "/articles/2018/08"
                "/restful-api-design-13-best-practices-to-make-your-users-happy/"
            ),
        ),
        (
            "/breaking-news-everything-is-an-event",
            "/articles/2018/09/breaking-news-everything-is-an-event/",
        ),
        (
            "/building-a-streaming-fraud-detection-system-with-kafka-and-python",
            (
                "/articles/2018/09"
                "/building-a-streaming-fraud-detection-system-with-kafka-and-python/"
            ),
        ),
        (
            "/consuming-apis-in-angular-the-model-adapter-pattern",
            "/articles/2018/09/consuming-apis-in-angular-the-model-adapter-pattern/",
        ),
        (
            "/streaming-applications-with-apache-kafka-the-opening",
            "/articles/2018/10/streaming-applications-with-apache-kafka-the-opening/",
        ),
        (
            "/from-angular-to-vue-feeling-like-a-beginner-again",
            "/articles/2018/10/from-angular-to-vue-feeling-like-a-beginner-again/",
        ),
        (
            "/inbox-zero-how-to-keep-clean-email-inbox-and-mind",
            "/articles/2018/10/inbox-zero-how-to-keep-clean-email-inbox-and-mind/",
        ),
        (
            "/reconciling-dataclasses-and-properties-in-python",
            "/articles/2018/10/reconciling-dataclasses-and-properties-in-python/",
        ),
        (
            "/how-i-built-a-web-framework-and-became-an-open-source-maintainer",
            (
                "/articles/2018/12"
                "/how-i-built-a-web-framework-and-became-an-open-source-maintainer/"
            ),
        ),
        (
            "/consuming-apis-in-angular-displaying-data-in-components",
            (
                "/articles/2019/02"
                "/consuming-apis-in-angular-displaying-data-in-components/"
            ),
        ),
        (
            "/real-time-chatbot-server-python-bocadillo",
            "/articles/2019/03/real-time-chatbot-server-python-bocadillo/",
        ),
        (
            "/attending-tech-conferences-beginner-guide",
            "/articles/2019/05/attending-tech-conferences-beginner-guide/",
        ),
        (
            "/why-i-dont-write-on-medium",
            "/articles/2019/05/why-i-dont-write-on-medium/",
        ),
        (
            "/introducing-tartiflette-starlette",
            "/articles/2019/07/introducing-tartiflette-starlette/",
        ),
        (
            # Article was actually published in June.
            "/articles/2019/07/vuepress-upgrade-1-0",
            "/articles/2019/06/vuepress-upgrade-1-0/",
        ),
        ("/vuepress-upgrade-1-0", "/articles/2019/06/vuepress-upgrade-1-0/"),
        (
            "/introduction-to-asgi-async-python-web",
            "/articles/2019/08/introduction-to-asgi-async-python-web/",
        ),
        (
            "/python-optionally-parametrized-decorators",
            "/articles/2019/09/python-optionally-parametrized-decorators/",
        ),
    ],
)
async def test_legacy_redirect_articles(
    client: TestClient, blog_dot_dev_path: str, dot_dev_path: str,
) -> None:
    resp = await client.get(
        f"https://blog.florimond.dev{blog_dot_dev_path}", allow_redirects=True
    )
    assert resp.status_code == 200
    assert resp.url == f"https://florimond.dev/blog{dot_dev_path}"
