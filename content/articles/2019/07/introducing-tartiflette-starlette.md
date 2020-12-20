---
published: true
title: "Introducing tartiflette-starlette"
description: "A new library for building GraphQL APIs and serving them over HTTP via ASGI, powered by the Tartiflette Python asynchronous GraphQL engine."
date: "2019-07-13"
legacy_url: "/introducing-tartiflette-starlette"
category: retrospectives
tags:
  - python
  - webdev
  - asgi
image: "/static/img/articles/tartiflette-starlette.jpg"
image_caption: "Logo of tartiflette-starlette."
---

For some reason, my recent open source work has been focusing on the Python asynchronous GraphQL ecosystem. A few months ago, I stumbled upon [Tartiflette], a Python 3.6+ async GraphQL engine built on top of `libgraphqlparser`. I got hooked up, and decided to contribute. Mix this with my previous experience with ASGI [gained from building Bocadillo](/blog/articles/2018/12/how-i-built-a-web-framework-and-became-an-open-source-maintainer), and the result is **[tartiflette-starlette]**.

[tartiflette]: https://tartiflette.io
[tartiflette-starlette]: https://github.com/tartiflette/tartiflette-starlette

## Features

`tartiflette-starlette` allows you to build GraphQL APIs with Python and Tartiflette and then serve it using any ASGI web server. The API design is inspired by the design principles behind Starlette and ASGI — clean, explicit, and composable.

Here, take a look:

```python
import asyncio
from tartiflette import Resolver, Subscription
from tartiflette_starlette import TartifletteApp


sdl = """
type Query {
  hello: String
}

type Subscription {
  timer(seconds: Int!): Timer
}

enum Status {
  RUNNING
  DONE
}

type Timer {
  remainingTime: Int!
  status: Status!
}
"""


@Resolver("Query.hello")
async def hello(parent, args, context, info):
    name = args["name"]
    return f"Hello, {name}!"


@Subscription("Subscription.timer")
async def on_timer(parent, args, context, info):
    seconds = args["seconds"]
    for i in range(seconds):
        yield {"remainingTime": seconds - i, "status": "RUNNING"}
        await asyncio.sleep(1)
    yield {"remainingTime": 0, "status": "DONE"}


app = TartifletteApp(sdl=sdl, subsriptions=True)
```

If you save this as `graphql.py`, you get a production-ready GraphQL API with the following features:

[uvicorn]: https://www.uvicorn.org

- **Compatibility with any ASGI web server**. For example, run `$ uvicorn graphql:app` to serve it using [uvicorn].
- **Built-in [GraphiQL] client** for in-browser interactive queries:

[graphiql]: https://github.com/graphql/graphiql

![](/static/img/tartiflette-starlette-graphiql-query.png)

- **Support for [GraphQL subscriptions](https://graphql.org/blog/subscriptions-in-graphql-and-relay/) over WebSocket**, with compatibility for GraphiQL client, [Apollo GraphQL](https://www.apollographql.com/) and any other client that implements the [subscriptions-transport-ws] protocol.

[subscriptions-transport-ws]: https://github.com/apollographql/subscriptions-transport-ws

![](/static/img/tartiflette-starlette-graphiql-subscription.png)

There are many more options to `TartifletteApp`, including passing a custom Tartiflette `Engine`, or customizing the `GraphiQL` configuration. You can learn about all the available features in the [documentation](https://github.com/tartiflette/tartiflette-starlette) on GitHub.

## Embracing ASGI

`tartiflette-starlette` embraces ASGI as a standard interface between Python asynchronous web servers and applications.

The introduction example works because `TartifletteApp` is an ASGI3-compliant application, and as such it can be served by any ASGI web server, including [uvicorn], [hypercorn](https://github.com/pgjones/hypercorn) and [daphne](https://github.com/django/daphne).

Besides, `tartiflette-starlette` is dead-easy to integrate against any ASGI web framework. For example, Bocadillo has a [GraphQL with Tartiflette](https://bocadilloproject.github.io/how-to/graphql.html) guide that shows how to mount a `TartifletteApp` as a sub-application, serving it along with the main Bocadillo application.

(Don't let the name fool you — `tartiflette-starlette` is not particularly tied to [Starlette], which it only uses as a lightweight ASGI toolkit.)

[starlette]: https://www.starlette.io

## Roadmap

I started working on `tartiflette-starlette` in April 2019. The initial goal was to add ASGI support to Tartiflette, which could then only be served using `aiohttp` using the [tartiflette-aiohttp](https://github.com/tartiflette/tartiflette-aiohttp) official wrapper. The first version was literally built in a few hours, but it was rather rudimentary.

Since then, feature parity has been reached — all features available in `tartiflette-aiohttp` are now also available in `tartiflette-starlette`.

The latest addition is GraphQL subscriptions over WebSocket. `tartiflette-starlette` implements the [subscriptions-transport-ws] protocol, a generic and reusable implementation of which has been extracted into [subscriptions-transport-ws-python](https://github.com/florimondmanca/subscriptions-transport-ws-python) and should be ported back into `tartiflette-starlette` very soon.

I feel like there's not much left to be done with `tartiflette-starlette`. Although it will require maintenance (as all software projects), it is already very much a finished product. Still, feel free to [try it out](https://github.com/tartiflette/tartiflette-starlette) and share feedback!

## Wrapping up

I feel proud of what has been achieved so far, mostly because I managed to pull all of this off without initial knowledge about GraphQL or its ecosystem. I learnt a lot in the process, which has definitely been one of the key motivation drivers.

Besides, `tartiflette-starlette` is the result of a collaboration with the engineers who work on Tartiflette full-time, and I want to thank Stan, Aurélien and Maxime (yep, all people involved in this story are French) for their support and feedback.

I started my final year internship about the time when I began working on `tartiflete-starlette`. Yet, my open source activity has been at an almost all-time high. Bocadillo is still under development, and I also manage to find some time for [djangorestframework-api-key](https://florimondmanca.github.io/djangorestframework-api-key/). Lots of exciting open source work ahead!
