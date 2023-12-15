---
title: "Structuring Starlette Projects"
description: "Starlette's modular design doesn't necessarily make it clear how Starlette projects should be structured. Here is a minimal yet flexible project structure that will prevent circular dependencies and help you write more readable Starlette application code."
date: "2020-06-01"
category: tutorials
tags:
  - python
  - webdev
  - asgi
image: "/static/img/articles/starlette-structure.jpg"
image_thumbnail: __auto__
image_caption: "@jjying, unsplash.com"
---

I think [Starlette](https://www.starlette.io/) is a wonderful little [ASGI](/blog/articles/2019/08/introduction-to-asgi-async-python-web/) framework. Its modular design is a true blessing for understanding individual components and how they all fit together.

But modularity can also be a curse when it comes to structuring applications, as the framework gives you total freedom there. E.g. one complication I came across early on was avoiding circular dependencies.

Over time I noticed a pattern in how I structure my Starlette projects which avoids these issues and has proven to be flexible enough for most use cases.

## Separation of concerns to the rescue

The core principle behind structuring Starlette projects is **separation of concerns**.

To avoid circular dependencies, we need to separate _logical domains_ of the application — configuration, views, routes, middleware, etc. — into their own Python modules.

Sounds abstract? Yup, sorry. Okay then, let me show you some code to illustrate what this means in practice. We'll build a sample Starlette app from the ground up, and see how we can structure things as our project becomes more and more fleshed out.

## Hello, app!

Let's start with a "Hello, world!" application:

```python
# app.py
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def home():
    return PlainTextResponse("Hello, world!")


routes = [
    Route("/", home, name="home"),
]

app = Starlette(routes=routes)
```

Clean and tidy, right? For quick-and-dirty single-endpoint apps, this works great.

But for applications with multiple routes, this "everything in one script" style can make things quickly get out of hand.

So how can we try and add some basic structure to this application?

## Splitting into modules

Let's take a closer look at the different steps we're taking here:

```python
# app.py
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


# 1. Declare a view.
async def home():
    return PlainTextResponse("Hello, world!")


# 2. Put it in a routing table.
routes = [
    Route("/", home, name="home"),
]

# 3. Declare the application instance.
app = Starlette(routes=routes)
```

As you can see, each step is fairly independent from the others.

So one sensible thing to do might be to create one Python module for each step.

Enters `views.py`:

```python
# views.py
from starlette.responses import PlainTextResponse


async def home(request):
    return PlainTextResponse("Hello, world!")
```

Then `routes.py`:

```python
# routes.py
from starlette.routing import Route
from . import views

routes = [
    Route("/", views.home, name="home"),
]
```

And lastly `app.py`:

```python
# app.py
from starlette.applications import Starlette

from .routes import routes

app = Starlette(routes=routes)
```

This is 3 files instead of 1, but on the other hand our project just gained structure and clear separation of concerns. We could now add as many views and routes as we'd like, and yet the overall structure of the project would stay the same.

## Adding templates

Now let's suppose we want the `home()` view to not return plain text, but instead an HTML page, probably with some static CSS and JS files to make it pretty and interactive.

Let's start with the HTML template, which we'll put in a `templates/` directory. We could edit `views.py` as follows:

```python
# views.py
from pathlib import Path
from starlette.responses import PlainTextResponse
from starlette.templating import JinjaTemplates

templates = JinjaTemplates(directory=str(Path(__file__).parent / "templates"))


async def home(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context=context)
```

Now for CSS and JS files located in a `static/` directory, we could edit `routes.py` as such:

```python
# routes.py
from pathlib import Path
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from . import views

static = StaticFiles(directory=str(Path(__file__).parent / "static"))

routes = [
    Route("/", views.home, name="home"),
    Mount("/static", static, name="static"),
]
```

Right away you can probably notice that we duplicate some logic when computing the `static` and `templates` directories — namely we're computing the base project directory twice.

Besides, it's also a bit of a smell that we're making path operations in the views and routing code.

So let's clean things up.

## Separating out configuration

We have here a good opportunity to separate these pieces of information into a new module, one that'll be specifically targeted at defining project configuration.

Enters `settings.py`:

```python
from pathlib import Path

BASE_DIR = Path(__file__).parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
```

Now we can go back and update `views.py` and `routes.py`:

```python
# views.py
from starlette.responses import PlainTextResponse
from starlette.templating import JinjaTemplates
from . import settings

templates = JinjaTemplates(directory=str(settings.TEMPLATES_DIR))

# ...
```

```python
# routes.py
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from . import views, settings

static = StaticFiles(directory=str(settings.STATIC_DIR))

# ...
```

Super — the `settings.py` module acts as a single source of truth for project configuration. The other modules can now import this configuration and wire it up however they'd like.

## Adding configurable debug mode

Now that we have an HTML template view, maybe we'd want to use Starlette's debug mode to show us some pretty in-browser tracebacks during development. We wouldn't want to turn it on in production though, so this is typically a good use case for an **environment variable**.

One way to derive configuration from environment variables in Starlette is using the `Config` helper.

Let's use it to add a new `DEBUG` setting:

```python
# settings.py
from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
# ...
```

We can now wire it up in the application script like so:

```python
from starlette.applications import Starlette
from . import settings

app = Starlette(
    debug=settings.DEBUG,
    # ...
)
```

Voilà! Now we can do:

```bash
DEBUG=true uvicorn server.app:app
```

and debug tracebacks will show up in case of server error.

Even better — we can keep a private git-ignored `.env` file, and let Starlette's `Config` helper read it automatically:

```bash
# .env
DEBUG=true
```

```bash
uvicorn server.app:app  # DEBUG is read from .env
```

We can use this pattern whenever we need something to be configurable through an environment variable. Neat, eh?

## Adding an HTTP client

We've gone a long way already in terms of structuring our app, but let's go one step further and see what we should do when we need access to a shared resource.

For example, let's say our app needs to make external web requests — maybe we have a view that acts as a proxy to another website, or one that fetches data from a web API. My go-to library for that now is [HTTPX](https://github.com/encode/httpx).

A working approach would be to create one client for each request, e.g.:

```python
# views.py
import httpx
from starlette.responses import HTMLResponse, JSONResponse
from . import settings


async def example_dot_com(request):
    async with httpx.AsyncClient() as client:
        url = "https://example.org"
        response = await client.get(url)

    return HTMLResponse(response.text)


async def search_movies(request):
    q = request.path_params["q"]

    async with httpx.AsyncClient() as client:
        url = "https://api.example.io/movies"
        params = {"api_key": settings.SOME_API_KEY, "q": q}
        response = await client.get(url, params=params)

    return JSONResponse(response.json())
```

But instead of creating a client each time, it would be better to reuse a shared `client` instance. We'd bnefit from HTTPX's connection pooling, which would reduce execution time and save up resources.

So one way we could go about this would be to declare a shared `client` instance at the top-level:

```python
# views.py
import httpx

client = httpx.AsyncClient()


async def example_dot_com(request):
    response = await client.get(...)
    # ...


async def search_movies(request):
    response = await client.get(...)
    # ...
```

Great — we're now sharing HTTP connections across calls to our app!

## Beware of circular imports

But what if we'd _also_ like to access the HTTP client in a separate module?

Maybe we've got a separate API service class for encapsulating requests to `someapi.io`, and it needs to make web requests too.

We'd probably define it in nicely separated out module. The HTTP `client` is defined in `views.py` so we'd have to import it from there:

```python
# example_api.py
from .views import client


class ExampleAPI:
    def __init__(self, client):
        self.client = client

    async def search_movies(self, query: str):
        params = {"q": query}
        response = await self.client.get("https://api.example.io/movies", params=params)
        # ...


example_api = ExampleAPI(client)
```

And then we'd use it in `views.py` like so…

```python
# views.py
import httpx
from starlette.responses import JSONResponse
from .example_api import example_api

client = httpx.AsyncClient()


async def search_movies(request):
    q = request.path_params["q"]
    movies = await example_api.search_movies(query=q)
    # ...
```

Notice how `example_api.py` imports something from `views.py` which itself imports something from `example_api.py`, now?

Tada! Circular imports. 😕

## Separating out shared resources

Okay, so maybe we can instead define the `client` in `example_api.py` and _then_ import that in `views.py`?

```python
# example_api.py
import httpx

client = httpx.AsyncClient()

# ...

example_api = ExampleAPI(client)
```

```python
# views.py
from .example_api import client

# ...
```

Sure — it would probably _work_. But it doesn't feel clean either, does it?

So… there must be a better way.

What we need to realize here is that by wanting to declare the shared HTTP client instance _in modules that use that shared client_, we're once again breaking separation of concerns.

Instead, what we should do is create a new module specifically for "here are resources shared across the application".

Enters `resources.py`:

```python
# resources.py
import httpx

client = httpx.AsyncClient()
```

Doesn't look like much, but now `views.py` and `example_api.py` can both import the `client` from `resources.py`, and everything falls into place nicely — no more circular imports!

```python
# example_api.py
import httpx
from . import resources

# ...

example_api = ExampleAPI(client=resources.client)
```

```python
# views.py
from starlette.responses import HTMLResponse, JSONResponse
from .example_api import example_api
from .resources import client


async def example_dot_com(request):
    response = await client.get(...)
    # ...


async def search_movies(request):
    q = request.path_params["q"]
    movies = await example_api.search_movies(query=q)
    # ...
```

## Adding more resources

Now that we have a module for shared application resources, it actually feels like the `templates` and `static` components from earlier could also be moved there, right?

Let's go for it:

```python
# resources.py
import httpx
from starlette.staticfiles import StaticFiles
from starlette.templating import JinjaTemplates
from . import settings

client = httpx.AsyncClient()

templates = JinjaTemplates(directory=str(settings.TEMPLATES_DIR))

static = StaticFiles(directory=str(settings.STATIC_DIR))
```

And now `views.py` and `routes.py` would look like this:

```python
# views.py
from .resources import templates


async def home(request):
    # ...
    return templates.TemplateResponse(...)
```

```python
# routes.py
from starlette.routing import Mount
from .resources import static

routes = [
    # ...
    Mount("/static", static, name="static"),
]
```

Again, doesn't look like much, but consistently using each module according to their purpose is what allows us to create structure.

## Adding more components

By now we've got the basic principles for structuring our Starlette project going: one module per _logical domain_.

Logical domains we've seen so far are configuration, resources, views, routes, and application declaration.

But we can expand this principle further for other parts of a Starlette project.

For example, middleware could be nicely separated out in a `middleware.py` module:

```python
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

middleware = [
    Middleware(GZipMiddleware),
    Middleware(CORSMiddleware, allow_origins=["app.example.io"]),
    # ...
]
```

And wired up in `app.py` like so:

```python
# app.py
from starlette.applications import Starlette
from .middleware import middleware

app = Starlette(
    # ...
    middleware=middleware,
)
```

We could also create modules for [exception handlers](https://www.starlette.io/exceptions/) or [event handlers](https://www.starlette.io/events/).

For example, we might want to ensure that the HTTPX `AsyncClient` is properly closed when the app shuts down, so that any remaining connection resources are properly released.

To do that we can create an `event_handlers.py` module containing something like:

```python
# event_handlers.py
from .resources import client

on_startup = []
on_shutdown = [client.aclose]
```

And then wire it all up in `app.py` as follows:

```python
# app.py
from starlette.applications import Starlette
from .event_handlers import on_shutdown

app = Starlette(
    # ...
    on_startup=on_startup,
    on_shutdown=on_shutdown,
)
```

`on_startup` is empty for now, but we could fill it with startup callbacks from other resources.

## Zooming out

At this point we've reached a project file structure that looks something like this:

```console
.
└── server
    ├── __init__.py
    ├── app.py
    ├── event_handlers.py
    ├── middleware.py
    ├── resources.py
    ├── routes.py
    ├── settings.py
    └── views.py
```

Believe it or not, but this structure has actually covered most of my needs when building out Starlette applications.

Not convinced yet? Let's expand our sample project just one more time and see how we'd go about adding a database client.

## Case study: adding a database client

Suppose we want to use the [Databases](https://www.encode.io/databases/) library to talk to a database, e.g. in order to make some of our web pages more dynamic.

So, how would we got about that?

Well, first of all the app would need to know where the database is located so that it can connect to it.

To do so we must to define the database URL somewhere, and it should be configurable (the database instance will certainly be different between production and our development environment).

All of this sounds an awful lot like a new setting! Here, let's add it:

```python
# settings.py
from databases import DatabaseURL
from starlette.config import Config

config = Config(".env")

# ...

DATABASE_URL = config(
    "DATABASE_URL", cast=DatabaseURL, default="postgresql://localhost/db"
)
```

Cool stuff. We can now go ahead and define the database client instance.

We may need to make database queries from multiple places, so it makes sense to treat the database client as a shared resource, which leads us to updating the `resources.py` module:

```python
from databases import Database
from . import settings

database = Database(settings.DATABASE_URL)

# ...
```

Nice! We can now go ahead and use the database client, e.g. maybe update the `home()` view to query articles for use when rendering the template:

```python
from .resources import database, templates


async def home(request):
    query = "SELECT * FROM articles"
    articles = await database.fetch_all(query)
    context = {"request": request, "articles": articles}
    return templates.TemplateResponse("index.html", context=context)
```

Super clean, huh?

Oh but let's not forget that the database connection needs to be initialized! It's about time we update the `event_handlers.py` module:

```python
from .resources import database

on_startup = [
    # ...
    database.connect,
]

on_shutdown = [
    # ...
    database.disconnect,
]
```

And… that's it. The database instance is configurable, accessible throughout the project, and cleanly setup and torn down on application startup and shutdown.

Note that we didn't have to change the application declaration, or any other part that isn't directly impacted by the definition of the database client.

Everything in its own place. 🧹

## That's all, folks!

There you go — we've seen how to structure a Starlette project with the following components:

- Project configuration: `settings.py`.
- Shared resources: `resources.py`.
- Views, routes, middleware, event handlers, etc.:`views.py`, `routes.py`, `middleware.py`, `event_handlers.py`, etc.
- Wiring everything up in an application declaration: `app.py`

Fear circular imports no more, and go build awesome stuff with Starlette!

P.S.: take a look at [the code for this blog](https://github.com/florimondmanca/www) or the [HostedAPI](https://github.com/encode/hostedapi) project if you're interested in seeing the code of real-world applications that use the structure discussed here.
