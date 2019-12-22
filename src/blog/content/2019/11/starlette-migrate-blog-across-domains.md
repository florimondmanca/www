---
published: true
title: "Using Starlette to migrate my blog across domains"
description: "How I moved my blog to a different domain and URL structure while retaining SEO and integrating seamlessly with a static website generator — a case study of using Starlette and ASGI to build and glue web application components together."
date: "2019-11-16"
tags:
  - python
  - asgi
  - vuepress
  - meta
image: "https://images.unsplash.com/photo-1468276311594-df7cb65d8df6?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"
image_caption: "Milky way above body of water. @krisroller, unsplash.com"
---

I recently rebuilt my personal blog. The design has changed a bit, but that was not the main goal of the migration. Behind this change lies a complete revamp in architecture and technology stack. By migrating from Django + Angular to Starlette + VuePress, I managed to cut down the total lines of code 3x, and to migrate my blog to a different domain while retaining SEO and ensuring old URLs are still valid.

In this article, we'll see how the migration process went, and you'll hopefully learn some things about the ASGI ecosytem and using Starlette to build custom web applications.

_**Note**: all the code in this article was extracted from the code for this very website, [which is open source](https://github.com/florimondmanca/www)._

## Bits of history

Last year in July, [I built my personal blog](https://florimond.dev/blog/articles/2018/07/let-the-journey-begin/) using Angular and Django. The architecture was a SaaS-like frontend/backend duo, a REST API pushing data to a client-side app built with a JS framework.

At the time I already knew it was a ridiculous and over-engineered choice for a blog. But well, you know, I'm a geek, and I wanted to learn about building and deploying websites, so there I was.

But, [as I tweeted some time ago](https://twitter.com/florimondmanca/status/1111203979357241344?s=20), this architecture was soon starting to feel like a burden, like a legacy code base you don't want to touch in fear of breaking things. As I gained more experience building large-scale frontend/backend applications, I now realize a lot of the code there was _bad_ — especially in the frontend. Unclear architecture, insufficient separation of concerns, leaky abstractions, you name it.

On top of that, it was a lot of code, in two separate repositories, with two separate build and deployment pipelines.

I started fearing my own code, and fearing breaking things. While the backend was tested quite thoroughly, the frontend was not — at all.

There were also a bunch of features I didn't need. The blog features a back office with a Markdown editor with live preview, import and storage of images on S3, and of course authentication to allow _me_ to access that back office.

## Enter: static site generators

I felt a lot of the over-engineering could be reduced if I moved to a static website generated from plain Markdown files, that I could edit in my favorite text editor and store in a Git repo, instead of a database.

This idea of my blog being just a bunch of HTML/CSS/JS files served by Nginx or something was very attractive. In particular because it meant I could cut hosting costs, virtually reaching zero if deploying to Netlify or GitHub Pages.

So I set myself up for building the blog using [VuePress](https://vuepress.vuejs.org). I would write Markdown files, be able to add custom or more advanced features using embedded Vue components, and render all of it to plain static files.

![The VuePress logo.](https://vuepress.vuejs.org/hero.png)

The main difficulty was building the custom theme. I don't use a generic website template — my blog design is hand-crafted with good ol' CSS — so I needed to port the design from Angular to a [VuePress theme](https://vuepress.vuejs.org/theme/writing-a-theme.html). Although all I theoretically had to do was copy-paste Angular components and convert them to use the Vue `template`/`script`/`style` single-file component syntax, this took quite a while.

I was nearing the end of this work, when I suddenly realized something.

## Retaining website traffic

You see, even though it's no HN, my blog has _some_ traffic. I take some pride in knowing that it draws ~50 unique visitors per day. Some of it comes from organic search, but a lot of it comes from backlinks to some of my most popular articles (e.g. [The Model-Adapter Pattern](https://florimond.dev/blog/articles/2018/09/consuming-apis-in-angular-the-model-adapter-pattern/)). So, if I just went ahead and replaced the old site with a new one, I might risk losing — dare I write the holy accronym? — SEO.

The risk was even more real, because I wanted to migrate all of my personal websites to be under a unique domain, `florimond.dev`. At the time, I had a landing page at `florimond.dev/`, and my blog was served at `blog.florimond.dev/`.

So, how should I proceed in order not to break URL references, and retain the existing ranking on search engines?

The answer was **redirections**.

## The redirection problem

As it turns out, I had already moved domains in the past. For example, I moved from `florimondmanca.com` (which I still own) to `florimond.dev`. This was a root domain change, so at the time I got away with simple DNS-level 301 redirections (via [dokku-redirect](https://github.com/dokku/dokku-redirect)).

But this time, the goal was to move from `blog.florimond.dev` to `florimond.dev/blog/`. I also wanted to improve the URL structure, e.g. by embedding the publication date. Something like `florimond.dev/blog/articles/:yyyy/:mm/:slug`.

So DNS-level or even web-server-level redirections were not enough. I needed to manage redirection at the web application level.

The problem is, VuePress' router capabilities are quite limited. It _can_ do redirection between pages it knows about, but not much more. And embedding redirection into VuePress itself, while the end result was going to be a bunch of static files, certainly didn't feel right.

So this was probably a backend's responsability.

## Deciding on the backend tech

Django, which I had been using until then, could have handled these complex redirection cases. But I didn't need most of its features anymore. For example, I didn't need a database anymore since all articles were now plain Markdown files in a Git repo. So I wanted to try something more lightweight.

If you follow my open source activity, you know I've been deep into the Python async web ecosystem recently, in particular ASGI. (I wrote about it in my [Introduction to ASGI](https://florimond.dev/blog/articles/2019/08/introduction-to-asgi-async-python-web/).)

So it shouldn't come as a surprise that I went for [Starlette](https://www.starlette.io).

![The Starlette logo.](https://www.starlette.io/img/starlette.png)

## Application architecture

At first, I tried to replicate the frontend/backend architecture I had before. My idea was to have two apps:

- `blog`: serves VuePress' static files at `florimond.dev/blog`.
- `index`: landing page at `florimond.dev/`.

Then I'd mount them onto a single Starlette app. I'd then handle redirections using a custom ASGI middleware that would redirect requests made to `blog.florimond.dev/*` to `florimond.dev/blog/*`.

Overall, this strategy _could_ have worked.

But it quickly turned out to be too complicated, and prone to some limitations. For example, having consistent error handling between the two sub-apps was quite difficult.

The final architecture I went for is even simpler. In fact, it wouldn't have been that simple without what was brought by Starlette v0.13.

## Declarative routing and composition in Starlette

In 0.12 and before, Starlette provided and encouraged an imperative, decorator-based routing API, much like Flask and many other microframeworks.

In v0.13, a more declarative and compositional style was introduced.

Instead of writing:

```python
from starlette.applications import Starlette

app = Starlette()

@app.route("/")
async def home(request):
    ...
```

You can (should?) now write:

```python
from starlette.applications import Starlette
from starlette.routing import Route

async def home(request):
    ...

routes = [
    Route("/", home),
]

app = Starlette(routes=routes)
```

This example makes it look like this style produces more code (it probably does), but I particularly like that all routing is now centralized in a single list. This is very similar to what I had seen in the frontend world (e.g. [Vue Router uses this style](https://router.vuejs.org/guide/)), so it made a lot of sense.

This style is also _extremely explicit_. There's as few hidden magic as possible (if at all). Compare this to e.g. Django's list of `urlpatterns` that somehow become routes mounted on a global router.

It also encourages using more of Starlette's routing components. `Route` is an obvious one, but few probably know about `Mount`, the component that powered `app.mount()`.

The routing was now extremely straight-forward:

- A `Route` to `/` for the landing page.
- A `Mount` on `/static` for static assets (e.g. the HTML template and CSS for the landing page, and various meta assets), served by the `StaticFiles` component.
- A `Mount` on `/blog` for the blog sub-app.

This is what it looks like in code:

```python
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from .. import blog

static_files = StaticFiles("static")

async def home(request):
    ...

routes = [
    Route("/", home),
    Mount("/blog", blog.app, name="blog"),
    Mount("/static", static_files, name="static"),
]

app = Starlette(routes=routes)
```

Beautiful, isn't it?

Now, you might be wondering what the `blog` module imported at the top of the script is…

## Integrating with VuePress

Here's the file structure of the main directory of code:

```
src/www
├── __init__.py
├── blog
│   ├── __init__.py
│   ├── app.py
│   ├── middleware.py
│   ├── settings.py
│   └── site
└── web
    ├── __init__.py
    ├── app.py
    ├── endpoints.py
    ├── settings.py
    ├── static
    └── templates
```

The previous code snippets were an approximation for what's in `web/app.py`.

As you can see, `blog` is a separate Starlette application. The VuePress website (where, in particular, Markdown files for the articles are located) is located in the `site/` sub-directory.

Now, all `blog` is virtually doing is serving the `site/.vuepress/dist` folder that VuePress outputs when the website is compiled to static files. (There are obviously some more details to make sure the integration with VuePress is seamless. For example, this is why `settings.py` and `middleware.py` exist.)

Stripped down, `blog/app.py` looks a bit like this:

```python
import pathlib
from starlette.staticfiles import StaticFiles

dist = pathlib.Path() / "site" / ".vuepress" / "dist"
app = StaticFiles(directory=dist)
```

Then, the `app` is re-exported in `blog/__init__.py` so that I can refer to it as `blog.app` in the router.

## Aside: modularity in Starlette

I hope you start to see why I now find Starlette so enjoyable to work with — it's even super fun! Starlette provides well-defined, narrowly-scoped, orthogonal components that you can mix and match to satisfy your specific needs, without depending on ad-hoc framework feature. It's really refreshing.

The best thing is that all of this is powered by the ASGI interface. All of `Route`, `Mount`, `Starlette` and even `StaticFiles` are implemented the same way — a callable class that implements the ASGI callable signature:

```python
class ASGIComponent:
    async def __call__(self, scope, receive, send) -> None:
        ...
```

Anyway, needless to say that I love all. of. this.

But wait — there's more!

## Back to the redirection problem

Remember that one of my requirements was to be able to smoothly redirect from `blog.florimond.dev/*` to `florimond.dev/blog/*`?

This is the strategy I went for:

1. Perform a page-to-page redirection from `blog.florimond.dev` to `florimond.dev/blog`. So, for example, `blog.florimond.dev/some-article` should redirect to `florimond.dev/blog/some-article`.
1. Once on `florimond.dev/blog`, redirect pages that correspond to an article to their actual URL.

Starlette helped in both steps, but let me first describe how VuePress helped with step 2).

## Legacy URL mapping using VuePress plugins

When a user (or a machine such as a web crawler) tries to access one of the old article URLs, e.g. `blog.florimond.dev/let-the-journey-begin`, they will be redirected to `florimond.dev/blog/let-the-journey-begin`. This is step 1). But where they should _eventually_ be redirected is to `florimond.dev/blog/2018/07/let-the-journey-begin`, i.e. the URL where the VuePress router exposes the article.

So, how can I implement this mapping and ensure it correctly works _even if I change the location of the new article_? The solution I found was to use the article frontmatter.

VuePress allows to define a [YAML frontmatter](https://vuepress.vuejs.org/guide/frontmatter.html) at the top of each article Markdown file. This is metadata that, for example, I can use to my willing in my custom theme. For example, I have a `tags` field that lets me define tags to display along with the article, and also enables dynamically building tag pages (such as https://florimond.dev/blog/tag/python) thanks to a custom [VuePress plugin](https://vuepress.vuejs.org/plugin/). There's also a `published` field I use to not show half-finished articles while being able to commit and deploy them.

So here's what the frontmatter for one of the articles looks like:

```yaml
published: true
title: "Let the Journey begin"
description: "Hi! My name is Florimond. I will be your captain for the length of this journey. 👨‍✈️"
date: "2018-07-25"
tags:
  - meta
image:
  path: "https://images.unsplash.com/photo-1518415917-ae14f59265b3"
  caption: "Josh Withers, unsplash.com"
```

There's another feature of VuePress that's going to help us here. VuePress provides a [plugin system](https://vuepress.vuejs.org/plugin/) which allows to write small reusable pieces of logic. In particular, it allows to access the list of all pages _and their frontmatter_.

So, the way I decided to handle article redirection was add a custom `legacy_url` field to the frontmatter. It would refer to the path where the article was accessible back then, on `blog.florimond.dev`. For example:

```yaml
legacy_url: /let-the-journey-begin
```

I could then:

1. Write a VuePress plugin to gather the `legacy_url -> page_path` mapping (by processing the list of pages).
1. Output the result to a git-ignored JSON file at build time.
1. Load that JSON file into a Python dictionnary in the `blog` Starlette app.
1. Within the app, check whether the requested path is in the dictionary, and return a 301 redirect to the new path.

Brilliant!

## Performing redirection with Starlette and ASGI

Obviously, there was some rejigging needed on the `blog` app. In particular, it was still a regular `StaticFiles` instance. But extending it is possible if we go one level down — the ASGI level.

The first step was to wrap the `StaticFiles` app into a function-based ASGI app, so that I can perform further customization:

```python
from starlette.staticfiles import StaticFiles

static = StaticFiles(...)

async def app(scope, receive, send):
    await static(scope, receive, send)
```

Good, now onto adding path`checking and redirection:

```python
from starlette.datastructures import URL
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
# 👇 JSON file loaded into a dict
from .settings import BLOG_LEGACY_URL_MAPPING

static = StaticFiles(...)

async def app(scope, receive, send):
    if scope["path"] in BLOG_LEGACY_URL_MAPPING:
        mapped_path = BLOG_LEGACY_URL_MAPPING[scope["path"]]
        redirect_path = scope.get("root_path", "") + mapped_path

        response = RedirectResponse(
            URL(scope=scope).replace(path=redirect_path), status_code=301,
        )
        await response(scope, receive, send)
        return

    await static(scope, receive, send)
```

There are two new Starlette components we're seeing here:

- `URL`, a datastructure that provides a higher-level API over the URL-related fields of an ASGI `scope`.
- `RedirectResponse`, a respone class that performs HTTP redirection, and _also_ acts as an ASGI app.

Again, I think the result is beautiful and easy to read (even though it requires some knowledge of how ASGI works and what `scope` is and what's in there).

Some edits to the build scripts and new tests later, I now had the article redirection setup!

So this was step 2) of the redirect chain; let's get back to step 1).

## Domain redirection

The goal of step 1) was to redirect all requests to `blog.florimond.dev/<path>` to `florimond.dev/blog/<path>`. This is similar to a DNS-level domain redirection, except we need to add the `/blog/` section to the requested path, so not that easy to do that way.

Fortunately, Starlette has yet another great routing component up its sleeve: `Host`.

`Host` makes it possible to route requests made to a particular domain to a dedicated ASGI application. This was exactly what I needed! I could map `blog.florimond.dev` to an ASGI app that does the following:

- Extract the requested path.
- Prepend `/blog/` to it.
- Perform a redirection using `RedirectResponse`.

Awesome!

Since I _also_ wanted to perform domain redirection from my older `*.florimondmanca.com` domains to `*.florimond.dev`, I extracted this logic into a reusable ASGI app:

```python
from starlette.requests import Request
from starlette.responses import RedirectResponse

class DomainRedirect:
    def __init__(
        self,
        domain: str,
        status_code: int = 301,
        root_path: str = None,
    ):
        self.domain = domain
        self.status_code = status_code
        self.root_path = root_path

    async def __call__(self, scope, receive, send):
        assert scope["type"] == "http"

        request = Request(scope)
        url = request.url.replace(hostname=self.domain)
        if self.root_path:
            url = url.replace(path=self.root_path + request.url.path)

        response = RedirectResponse(url, status_code=self.status_code)
        await response(scope, receive, send)

```

That's a fair bunch of code, but bear with me.

An instance of `DomainRedirect` is an ASGI application (as can be seen from the `__call__(scope, receive, send)` method) that does the following:

- Ingest the requested URL into an `URL` instance.
- Pre-prend any root path specified on the endpoint (e.g. `/blog`).
- Perform the redirection.

The class-based style is a bit verbose, but at least it does exactly what I need.

I can then use `DomainRedirect` in combination with `Host` to register domain redirections:

```python
from starlette.routing import Host
from .endpoints import DomainRedirect

routes = [
    # ...
    Host(
        "blog.florimond.dev",
        DomainRedirect("florimond.dev", root_path="/blog"),
    ),
    # ...
]
```

That's it! Now, to add redirections from my older `*.florimondmanca.com` domains, all I have to do is add more `Host` entries to the list of `routes`:

```python
routes = [
    # ...
    Host("florimondmanca.com", DomainRedirect("florimond.dev")),
    Host("blog.florimondmanca.com", DomainRedirect("blog.florimond.dev")),
    # ...
]
```

_Lovely._

## Peek into the final Starlette app

So, what have we got? The resulting `app.py` script for the main application, stripped from non-essential features (error handling, monitoring middleware, …) is **just under 30 LOC**:

```python
from starlette.applications import Starlette
from starlette.routing import BaseRoute, Host, Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from .. import blog
from .endpoints import DomainRedirect

templates = Jinja2Templates(directory="templates")
static_files = StaticFiles(directory="static")

async def home(request):
    return templates.TemplateResponse("index.html.jinja", context={"request": request})

routes = [
    Host("florimondmanca.com", DomainRedirect("florimond.dev")),
    Host("blog.florimondmanca.com", DomainRedirect("blog.florimond.dev")),
    Host("blog.florimond.dev", DomainRedirect("florimond.dev", root_path="/blog")),
    Route("/", home),
    Mount("/blog", app=blog.app, name="blog"),
    Mount("/static", static_files, name="static"),
]

app = Starlette(routes=routes)
```

I don't know about you (I'm definitely starting to repeat myself), but I find all of this _extremely_ elegant.

Obviously, there's an entire other section of the repository — tests! — that I won't have time to talk about here. But hopefully I'll soon be able to write up about what testing looks like in the ASGI ecosystem, and how much I find [HTTPX](https://github.com/encode/httpx) to be helping in that regard. Suffice it to say say that all the legacy redirection logic is fully tested, and that only takes up another small 30-LOC pytest-based test script.

## Taking a step back

Overall, I'm super happy with how the migration went.

I'll admit that VuePress is not the simplest technology to go to for building static sites. But:

- I worked with it in the past, and I really enjoy the recent additions to VuePress 1.x. (I wrote about migrating to VuePress 1.x [here](https://florimond.dev/blog/articles/2019/07/vuepress-upgrade-1-0/).) Plugins makes extending the behavior of a VuePress site delightful, in particular thanks to page introspection.
- Most frontend technologies are quite complex anyway, and I haven't found a static site generator that's less complex than VuePress.

On the backend side, this is the first Starlette-based service I've actually put in production. I think the declarative style introduced in Starlette v0.13 is wonderful, and fits the general modularity-oriented ASGI mindset very well. The `Host` component is definitely one I'll keep an eye on, even though it's not documented yet.

Another interesting aspect of this work was project management. Overall, the migration took about 2 months to complete. I worked on it over weekends — a few hours here and there. To not end up with a huge dump of changes, I used a feature flag. This allowed me to deploy the partially-working blog besides the landing page, while preventing visitors and web crawlers from accessing it (and ruining my dear, dear SEO).

Finally, let's try to put some numbers on all of this. One motivation for rebuilding my website was to reduce maintenance burden and the sheer amount of code that I had just for a personal blog. How well did this do?

To find out, I compared the output of [cloc](https://github.com/AlDanial/cloc) on the old and new setup. `cloc` is a tool for counting lines of code, a metric that I hoped had been reduced thanks to the migration.

Here are the results:

| Stack                | LOC (total)      |
| -------------------- | ---------------- |
| Django + Angular     | 1.3k + 4.7k = 6k |
| Starlette + VuePress | 2.1k             |

If you like KPIs, here's one: the new setup has **3 times less lines of code**. No doubt here — it's definitely a more lightweight setup.

If we dig into the detail across languages on the new Starlette + VuePress setup, we see that **the Starlette app is only 1/10th** of the total amount of code:

| Language | LOC |
| -------- | --- |
| HTML     | 800 |
| Stylus   | 500 |
| Vue      | 340 |
| JS       | 270 |
| Python   | 140 |

All of this is about application code, but there were benefits on the infrastructure side too.

The main key result here is that the infrastructure got a lot more lightweight. [I still use Dokku](https://twitter.com/florimondmanca/status/1102155774841769985?s=20) to deploy and manage application containers running on my VM, but there's now only one container. It's a Gunicorn server that serves the Starlette app (which in turn serves the VuePress-built static assets). Compare this with the 3-container setup I had previously (backend API, frontend app, Postgres database), which was definitely more heavy-weight and resource-intensive.

The only downside is that I had to _temporarily_ upgrade the VM to 2GB RAM. (1GB was just not enough to allow VuePress to build the site at deploy time, which is the most convenient solution.) This means I the hosting price tag doubled. But I plan to update the deploy script so that it builds assets locally (on my computer), then `scp`s them to the VM somewhere Dokku can pick them up when deploying the app. This will allow me to downgrade back to 1GB RAM — more than enough for day-to-day operation of the app.

## Wrapping up

So, what's the takeaway from this article?

Here it is: Starlette (and the ever-growing set of librairies and frameworks within the ASGI ecosystem) are great if you want to glue things together into high-performance, lightweight web services. Some examples:

- In this article, I used Starlette to retain SEO by implementing domain redirection, while integrating seamlessly with VuePress, a JS-powered static site generator.
- Matt Layman used Starlette along with HTTPX to [mock an external service](https://www.mattlayman.com/blog/2019/starlette-mock-service/).
- [Datasette](https://github.com/simonw/datasette), built by Simon Willison, uses ASGI to serve SQLite databases over HTTP, making it easier to explore and publish open data.

So, what will _you_ build with Starlette? 😉

P.S.: if you'd like to see the code for this website, [it's open source](https://github.com/florimondmanca/www).
