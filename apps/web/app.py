from starlette.types import ASGIApp

from apps import feature_flags, index

from .middleware import SubdomainRedirectMiddleware


def get_app() -> ASGIApp:
    if feature_flags.BLOG_ENABLED:
        from apps import blog

        index.app.mount("/blog", app=blog.app)
        return SubdomainRedirectMiddleware(index.app, mapping={"blog": "/blog/"})
    return index.app


app = get_app()
