import typing

import httpx
import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "start_url, urls",
    [
        pytest.param(
            "http://florimondmanca.com",
            [("http://florimond.dev/", 301)],
            id="home",
        ),
        pytest.param(
            "http://blog.florimondmanca.com",
            [
                ("http://blog.florimond.dev/", 301),
                ("http://florimond.dev/blog/", 301),
                ("http://florimond.dev/", 307),
            ],
            id="blog:home",
        ),
        pytest.param(
            "http://blog.florimondmanca.com/let-the-journey-begin",
            [
                ("http://blog.florimond.dev/let-the-journey-begin", 301),
                ("http://florimond.dev/blog/let-the-journey-begin", 301),
                (
                    "http://florimond.dev/en/posts/2018/07/let-the-journey-begin/",
                    301,
                ),
            ],
            id="blog:article",
        ),
        pytest.param(
            "http://florimond.dev/blog/articles/2021/04/google-floc",
            [
                ("http://florimond.dev/en/posts/2021/04/google-floc/", 301),
            ],
            id="blog_articles:en_posts",
        ),
        pytest.param(
            "http://florimond.dev/blog/articles/2021/04/google-floc/",
            [
                ("http://florimond.dev/en/posts/2021/04/google-floc/", 301),
            ],
            id="blog_articles:en_posts-trailing_slash",
        ),
    ],
)
async def test_legacy_redirect_chains(
    client: httpx.AsyncClient, start_url: str, urls: typing.List[str]
) -> None:
    resp = await client.get(start_url, allow_redirects=True)
    assert resp.status_code == 200
    assert [(r.headers["Location"], r.status_code) for r in resp.history] == urls


@pytest.mark.parametrize(
    "legacy_path, path",
    [
        (
            "/let-the-journey-begin",
            "/en/posts/2018/07/let-the-journey-begin/",
        ),
        (
            "/a-practical-usage-of-chainmap-in-python",
            "/en/posts/2018/07/a-practical-usage-of-chainmap-in-python/",
        ),
        (
            "/cheap-and-easy-deployment-captainduckduck-1",
            "/en/posts/2018/07/cheap-and-easy-deployment-captainduckduck-1/",
        ),
        (
            "/why-i-started-using-python-type-annotations-and-why-you-should-too",
            "/en/posts/2018/07/why-i-started-using-python-type-annotations-and-why-you-should-too/",  # noqa
        ),
        (
            "/cheap-and-easy-deployment-captainduckduck-2",
            "/en/posts/2018/08/cheap-and-easy-deployment-captainduckduck-2/",
        ),
        (
            "/python-mutable-defaults-are-the-source-of-all-evil",
            "/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/",  # noqa
        ),
        (
            "/restful-api-design-13-best-practices-to-make-your-users-happy",
            "/en/posts/2018/08/restful-api-design-13-best-practices-to-make-your-users-happy/",  # noqa
        ),
        (
            "/breaking-news-everything-is-an-event",
            "/en/posts/2018/09/breaking-news-everything-is-an-event/",
        ),
        (
            "/building-a-streaming-fraud-detection-system-with-kafka-and-python",
            "/en/posts/2018/09/building-a-streaming-fraud-detection-system-with-kafka-and-python/",  # noqa
        ),
        (
            "/consuming-apis-in-angular-the-model-adapter-pattern",
            "/en/posts/2018/09/consuming-apis-in-angular-the-model-adapter-pattern/",  # noqa
        ),
        (
            "/streaming-applications-with-apache-kafka-the-opening",
            "/en/posts/2018/10/streaming-applications-with-apache-kafka-the-opening/",  # noqa
        ),
        (
            "/from-angular-to-vue-feeling-like-a-beginner-again",
            "/en/posts/2018/10/from-angular-to-vue-feeling-like-a-beginner-again/",
        ),
        (
            "/inbox-zero-how-to-keep-clean-email-inbox-and-mind",
            "/en/posts/2018/10/inbox-zero-how-to-keep-clean-email-inbox-and-mind/",
        ),
        (
            "/reconciling-dataclasses-and-properties-in-python",
            "/en/posts/2018/10/reconciling-dataclasses-and-properties-in-python/",
        ),
        (
            "/how-i-built-a-web-framework-and-became-an-open-source-maintainer",
            "/en/posts/2018/12/how-i-built-a-web-framework-and-became-an-open-source-maintainer/",  # noqa
        ),
        (
            "/consuming-apis-in-angular-displaying-data-in-components",
            "/en/posts/2019/02/consuming-apis-in-angular-displaying-data-in-components/",  # noqa
        ),
        (
            "/real-time-chatbot-server-python-bocadillo",
            "/en/posts/2019/03/real-time-chatbot-server-python-bocadillo/",
        ),
        (
            "/attending-tech-conferences-beginner-guide",
            "/en/posts/2019/05/attending-tech-conferences-beginner-guide/",
        ),
        (
            "/why-i-dont-write-on-medium",
            "/en/posts/2019/05/why-i-dont-write-on-medium/",
        ),
        (
            "/introducing-tartiflette-starlette",
            "/en/posts/2019/07/introducing-tartiflette-starlette/",
        ),
        (
            # Article was actually published in June.
            "/articles/2019/07/vuepress-upgrade-1-0",
            "/en/posts/2019/06/vuepress-upgrade-1-0/",
        ),
        (
            "/vuepress-upgrade-1-0",
            "/en/posts/2019/06/vuepress-upgrade-1-0/",
        ),
        (
            "/introduction-to-asgi-async-python-web",
            "/en/posts/2019/08/introduction-to-asgi-async-python-web/",
        ),
        (
            "/python-optionally-parametrized-decorators",
            "/en/posts/2019/09/python-optionally-parametrized-decorators/",
        ),
    ],
)
async def test_legacy_redirect_articles(
    client: httpx.AsyncClient,
    legacy_path: str,
    path: str,
) -> None:
    # blog.florimond.dev/xyz -> florimond.dev/en/posts/xyz
    resp = await client.get(
        f"https://blog.florimond.dev{legacy_path}", allow_redirects=True
    )
    assert resp.status_code == 200
    assert resp.url == f"https://florimond.dev{path}"

    # No such redirection for florimond.dev/xyz/ (these URLs have never existed).
    resp = await client.get(
        f"https://florimond.dev{legacy_path}/", allow_redirects=False
    )
    assert resp.status_code == 404
