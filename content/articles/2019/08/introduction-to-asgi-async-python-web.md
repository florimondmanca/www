---
published: true
title: "Introduction to ASGI: Emergence of an Async Python Web Ecosystem"
description: "If you were thinking Python had been getting locked into data science, think again! Python web development is back with an async spin, and it's exciting."
date: "2019-08-11"
legacy_url: "/introduction-to-asgi-async-python-web"
tags:
  - python
  - webdev
  - asgi
image: "https://images.unsplash.com/photo-1482642302383-7ba0f8012849?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1051&q=80"
image_caption: '"Turtles on body of water", Ricard Baraham via unsplash.com'
---

There's a lot of exciting stuff happening in the Python web development ecosystem right now — one of the main drivers of this endeavour is [ASGI], the Asynchronous Server Gateway Interface.

[asgi]: https://asgi.readthedocs.io/en/latest/

I already mentioned ASGI several times here, in particular when [announcing Bocadillo](/blog/articles/2018/12/how-i-built-a-web-framework-and-became-an-open-source-maintainer) and [tartiflette-starlette](/blog/articles/2019/07/introducing-tartiflette-starlette/), but I never really took the time to write a thorough introduction about it. Well, here we are!

This post is targeted at people interested in recent trends of Python web development. I want to take you on a guided tour about **what ASGI is** and **what it means for modern Python web development**.

Before we begin, I'd like to announce that I recently created [awesome-asgi], an _awesome list_ to help folks keep track of the ever-expanding ASGI ecosystem. 🙌

[![Click to see the repo on GitHub.](https://florimondmanca-personal-website.s3.amazonaws.com/media/markdownx/14da23c7-58aa-4008-9da0-9b2b879d0900.png)][awesome-asgi]

You can watch releases to be notified of new entries to the list. 👀

[awesome-asgi]: https://github.com/florimondmanca/awesome-asgi

Alright, let's dive in!

## It all started with async/await

Contrary to JavaScript or Go, Python is not a language that had asynchronous execution baked in from the start. For a long time, executing things concurrently in Python could only be achieved using multithreading or multiprocessing, or resorting to specialized networking libraries such as eventlet, gevent, or Twisted. (Back in 2008, Twisted already had APIs for asynchronous coroutines, e.g. in the form of [`inlineCallbacks` and `deferredGenerator`](http://blog.mekk.waw.pl/archives/14-Twisted-inlineCallbacks-and-deferredGenerator.html).)

But this all changed in Python 3.4+. Python 3.4 [added `asyncio` to the standard library](https://www.python.org/dev/peps/pep-3156), adding support for cooperative multitasking on top of generators and the `yield from` syntax.

Later, the `async`/`await` syntax was [added in Python 3.5](https://www.python.org/dev/peps/pep-0492/). Thanks to this, we now had **native coroutines** independent of the underlying implementation, which opened the gold rush towards Python concurrency.

And what a rush it was, indeed! Since 3.5 was released, the community has been literally **async-ifying all the things**. If you're curious, a lot of the resulting projects are now listed in [aio-libs](https://github.com/aio-libs) and [awesome-asyncio](https://github.com/timofurrer/awesome-asyncio).

Well, you guessed it — this also means that **Python web servers and apps are moving towards async**. In fact, all the cool kids are doing it! ([Even Django](https://github.com/django/deps/blob/master/accepted/0009-async.rst).)

## An overview of ASGI

Now, how does ASGI fit in all of this?

From a 1000-foot perspective, ASGI can be thought of as the glue that allows Python asynchronous servers and applications to communicate with each other. It shares a lot of design ideas with [WSGI], and is often presented as its spiritual successor with async built-in.

[wsgi]: https://www.python.org/dev/peps/pep-3333

Here's what this mental model looks like in a diagram:

![At a very high-level, ASGI is a communication interface between apps and servers.](https://thepracticaldev.s3.amazonaws.com/i/c45c65uug0ezbqyf5rvl.png)

But in reality, it's a bit more complex than that.

To find out how ASGI really works, let's take a look at the [ASGI specification](https://asgi.readthedocs.io/en/latest/specs/main.html#overview):

> ASGI consists of two different components:
>
> - A _protocol server_, which terminates sockets and translates them into connections and per-connection event messages.
> - An _application_, which lives inside a _protocol server_, is instanciated once per connection, and handles event messages as they happen.

So according to the spec, what ASGI really specifies is a [message format](https://asgi.readthedocs.io/en/latest/specs/www.html) and how those messages should be exchanged between the application and the protocol server that runs it.

We can now revise our diagram into a more detailed version:

![How ASGI *really* works.](https://thepracticaldev.s3.amazonaws.com/i/2mw06bobv5sjjc0r1omb.png)

There are many more interesting details to look at, obviously. For example, you can take a look at the [HTTP and WebSocket specification](https://asgi.readthedocs.io/en/latest/specs/www.html).

Besides, although the spec focuses a lot on server-to-application communication, ASGI turns out to encompass _much more_ than that.

We'll get to this in a minute, but first…

## ASGI basics

Now that we've seen how ASGI fits in the Python web ecosystem, let's take a closer look at what it looks like in code.

ASGI relies on a simple mental model: when the client connects to the server, we instanciate an application. We then feed incoming bytes into the app and send back whatever bytes come out.

"Feed into the app" here really means _call the app_ as if it were a function, i.e. something that takes some input, and returns an output.

And in fact, that's all an ASGI app is — a _callable_. The shape of this callable is, again, [defined by the ASGI spec](https://asgi.readthedocs.io/en/latest/specs/main.html#applications). Here's what it looks:

```python
async def app(scope, receive, send):
    ...
```

The signature of this function is what the "I" in ASGI stands for: an interface which the application must implement for the server to be able to call it.

Let's take a look at the 3 arguments:

- `scope` is a dictionary that contains information about the incoming request. Its contents vary between [HTTP](https://asgi.readthedocs.io/en/latest/specs/www.html#connection-scope) and [WebSocket](https://asgi.readthedocs.io/en/latest/specs/www.html#id1) connections.
- `receive` is an asynchronous function used to receive _ASGI event messages_.
- `send` is an asynchronous function used to send ASGI event messages.

In essence, these arguments allow you to `receive()` and `send()` data over a communication channel maintained by the protocol server, as well as know in what context (or `scope`) this channel was created.

I don't know about you, but the overall look and shape of this interface fits my brain really well. Anyway, time for code samples.

## Show me the code!

To get a more practical feel of what ASGI looks like, I created a minimal project which showcases a raw ASGI HTTP app served by [uvicorn] (a popular ASGI server):

[uvicorn]: https://www.uvicorn.org/

[![Click to see and edit the code on Glitch.](https://florimondmanca-personal-website.s3.amazonaws.com/media/markdownx/439bffd8-a90b-4b22-ae6c-826baf74aa1a.png)](https://glitch.com/edit/#!/asgi-hello-world)

Here, we use `send()` to send an HTTP response to the client: we send headers first, and then the response body.

Now, with all these dictionaries and raw binary data, I'll admit that bare-metal ASGI isn't very convenient to work with.

Luckily, there are higher-level options — and that's when I get to talk about [Starlette].

[starlette]: https://www.starlette.io/

Starlette is truly a fantastic project, and IMO a foundational piece of the ASGI ecosystem.

In a nutshell, it provides a toolbox of higher-level components such as requests and responses that you can use to abstract away some of the details of ASGI. Here, take a look at this Starlette hello world:

```python
# app.py
from starlette.responses import PlainTextResponse


async def app(scope, receive, send):
    assert scope["type"] == "http"
    response = PlainTextResponse("Hello, world!")
    await response(scope, receive, send)
```

Starlette does have everything you'd expect from an actual web framework — routing, middleware, etc. But I decided to show this stripped-down version to hint you at the real power of ASGI, which is…

## Turtles all the way down

The interesting and downright _game-changing_ bit about ASGI is the concept of "[Turtles all the way down](https://simonwillison.net/2019/Jun/23/datasette-asgi/)", an expression originally coined (I think?) by Andrew Godwin, the person behind Django migrations and now the [Django async revamp](https://www.youtube.com/watch?v=oMHrDy62kgE).

But what does it mean, exactly?

Well, because ASGI is an abstraction which allows to tell in which context we are and to receive and send data _at any time_, there's this idea that ASGI can be used not only between servers and apps, but really _at any point in the stack_.

For example, the Starlette `Response` object _is_ an ASGI application itself. In fact, we can strip down the Starlette example app from earlier to _just this_:

```python
# app.py
app = PlainTextResponse("Hello, world!")
```

How _ridiculous_ is that?! 😍

But wait, there's more.

The deeper consequence of "Turtles all the way down" is that we can build all sorts of applications, middleware, libraries and other projects, and ensure that they will be **interoperable** as long as they all implement the ASGI application interface.

(Besides, from my own experience building [Bocadillo](https://bocadilloproject.github.io/), embracing the ASGI interface very often (if not _always_) results in much cleaner code.)

For example, we can build a ASGI middleware (i.e. an app that wraps another app) to display the time a request took to be served:

```python
# app.py
import time


class TimingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start_time = time.time()
        await self.app(scope, receive, send)
        end_time = time.time()
        print(f"Took {end_time - start_time:.2f} seconds")
```

To use it, we simply wrap it around an app…

```python
# app.py
import asyncio
from starlette.responses import PlainTextResponse


async def app(scope, receive, send):
    await asyncio.sleep(1)
    response = PlainTextResponse("Hello, world!")
    await response(scope, receive, send)


app = TimingMiddleware(app)
```

…and it will magically _just work_.

```bash
$ uvicorn app:app
INFO: Started server process [59405]
INFO: Waiting for application startup.
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
...
INFO: ('127.0.0.1', 62718) - "GET / HTTP/1.1" 200
Took 1.00 seconds
```

The amazing bit about this is that `TimingMiddleware` can wrap _any_ ASGI app. The inner app here is super simple, but it could be _a full-blown, real-life project_ (think hundreds of API and WebSocket endpoints) — it doesn't matter, as long as it's ASGI-compatible.

(There's a more production-ready version of such a timing middleware: [timing-asgi](https://github.com/steinnes/timing-asgi).)

## Why should I care?

While I think interoperability is a strong selling point, there are many more advantages to using ASGI-based components for building Python web apps.

- Speed: the async nature of ASGI apps and servers make them [really fast](https://www.techempower.com/benchmarks/#section=data-r18&hw=ph&test=fortune&l=zijzen-f&w=zik0zh-zik0zj-e7&d=b) (for Python, at least) — we're talking about 60k-70k req/s (consider that Flask and Django only achieve 10-20k in a similar situation).
- Features: ASGI servers and frameworks gives you access to inherently concurrent features (WebSocket, Server-Sent Events, HTTP/2) that are impossible to implement using sync/WSGI.
- Stability: ASGI as a spec has been around for about 3 years now, and version 3.0 is considered very stable. Foundational parts of the ecosystem are stabilizing as a result.

In terms of libraries and tooling, I don't think we can say we're there _just yet_. But thanks to a very active community, I have strong hopes that the ASGI ecosystem reaches feature parity with the traditional sync/WSGI ecosystem real soon.

## Where can I find ASGI-compatible components?

In fact, more and more people are building and improving projects built around ASGI. This includes servers and web frameworks obviously, but also middleware and product-oriented applications such as [Datasette](https://github.com/simonw/datasette).

Some of the non-web framework components that I got the most excited about are:

- [Mangum](https://github.com/erm/mangum): ASGI support for AWS Lambda
- [datasette-auth-github](https://github.com/simonw/datasette-auth-github): GitHub authentication for ASGI apps
- [tartiflette-starlette](https://github.com/tartiflette/tartiflette-starlette) (I wrote this one!): ASGI support for Tartiflette, an async GraphQL engine.

While seeing the ecosystem flourish is great, I've personally been having a hard time keeping up with everything.

That's why, as announced at the beginning of this article I created [awesome-asgi]. My hope is that it helps everyone keep up with all the awesome things that are happening in the ASGI space. (And seeing that it almost reached 100 stars in a few days, I have a feeling there was indeed a need to colocalize ASGI resources.)

## Wrapping up

While it might look like an implementation detail, I truly think that ASGI has laid down the foundations for a new era in Python web development.

If you want to learn more about ASGI, take a look at the various [publications](https://github.com/florimondmanca/awesome-asgi#publications) (articles and talks) listed in `awesome-asgi`. To get your hands dirty, try out any of the following projects:

- [uvicorn]: ASGI server.
- [Starlette]: ASGI framework.
- [TypeSystem](https://www.encode.io/typesystem/): data validation and form rendering
- [Databases](https://www.encode.io/databases/): async database library.
- [orm](https://github.com/encode/orm): asynchronous ORM.
- [HTTPX](https://www.encode.io/httpx/): async HTTP client w/ support for calling ASGI apps (useful as a test client).

These projects were built and are maintained by Encode, which mostly means Tom Christie. There are open discussions on setting up an [Encode maintenance team](https://discuss.encode.io/t/setting-up-a-maintainence-team/721/9), so if you were looking for an opportunity to help advance an open source niche, there you go!

Enjoy your ASGI journey. ❣️
