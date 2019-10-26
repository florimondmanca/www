from apps import feature_flags, index

from .middleware import LegacyBlogRedirectMiddleware

if feature_flags.BLOG_ENABLED:
    from apps import blog

    index.app.mount("/blog", app=blog.app)

app = LegacyBlogRedirectMiddleware(index.app)
