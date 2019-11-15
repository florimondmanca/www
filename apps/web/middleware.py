import tldextract
from starlette import status
from starlette.datastructures import URL, Headers
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class LegacyBlogRedirectMiddleware:
    """
    Redirect requests made to "blog.florimond.dev/..."
    to "florimond.dev/blog/articles/...".

    This ensures that robots (e.g. search engines) progressively update their
    indexes from old URLs to the new ones.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    def get_app(self, scope: Scope) -> ASGIApp:
        if scope["type"] != "http":
            return self.app

        headers = Headers(scope=scope)
        url = URL(scope=scope)
        host = headers["host"]
        extract = tldextract.extract(host)
        domain = extract.registered_domain
        subdomain = extract.subdomain

        if subdomain != "blog":
            return self.app

        redirect_url = url.replace(
            hostname=domain,
            path="/blog/" if url.path == "/" else f"/blog/articles{url.path}",
        )
        return RedirectResponse(
            url=str(redirect_url), status_code=status.HTTP_301_MOVED_PERMANENTLY
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        app = self.get_app(scope=scope)
        await app(scope, receive, send)
