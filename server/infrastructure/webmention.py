import httpx

from .. import settings


def get_webmention_io_client() -> httpx.AsyncClient:
    if settings.TESTING:
        return _webmention_mock_client()
    return httpx.AsyncClient()  # pragma: no cover


def _webmention_mock_client() -> httpx.AsyncClient:
    async def handler(_: httpx.Request) -> httpx.Response:
        post_url = "https://florimond.dev/en/posts/2018/07/let-the-journey-begin"

        html = (
            "<p>"
            '<a href="https://fosstodon.org/@florimond" class="u-test">@florimond</a> '
            "Great stuff!"
            "</p>"
        )

        return httpx.Response(
            200,
            json={
                "children": [
                    {
                        "type": "entry",
                        "author": {
                            "name": "John Doe",
                            "url": "https://fosstodon.org/@johndoe",
                        },
                        "in-reply-to": post_url,
                        "url": "https://fosstodon.org/@johndoe/123456",
                        "published": "2023-12-18",
                        "content": {"html": html},
                    },
                ]
            },
        )

    return httpx.AsyncClient(transport=httpx.MockTransport(handler))
