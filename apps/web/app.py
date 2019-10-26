from apps import blog, feature_flags, index

from .middleware import SubdomainRedirectMiddleware

if feature_flags.BLOG_ENABLED:
    index.app.mount("/blog", app=blog.app)

app = SubdomainRedirectMiddleware(index.app, mapping={"blog": "/blog/"})
