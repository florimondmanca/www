from starlette.applications import Starlette
from starlette.types import ASGIApp

from apps import blog, index
from .middleware import SubdomainRedirectMiddleware


app: ASGIApp
app = Starlette()
app.mount("/blog/", app=blog.app)
app.mount("/", app=index.app)
app = SubdomainRedirectMiddleware(app, mapping={"blog": "/blog/"})
