import asyncio
import importlib
import re
import sys
import traceback
from contextlib import AsyncExitStack
from typing import Any, NamedTuple, Sequence, Set
from urllib.parse import urldefrag, urljoin, urlsplit

import httpx


class Config(NamedTuple):
    root_url: str
    ignore: Sequence[str]
    client: httpx.AsyncClient
    limit: asyncio.BoundedSemaphore


class State(NamedTuple):
    todo: Set[str]
    busy: Set[str]
    done: Set[str]
    tasks: Set[asyncio.Future]


def replace_root(url: str, root_url: str) -> str:
    return urljoin(root_url, urlsplit(url).path)


async def crawl(
    root_url: str,
    output: str = "sitemap.xml",
    host: str = None,
    ignore: Sequence[str] = (),
    max_tasks: int = 100,
    client: httpx.AsyncClient = None,
    check: bool = False,
) -> int:
    client = httpx.AsyncClient() if client is None else client

    async with client:
        config = Config(
            root_url=root_url,
            ignore=[urljoin(root_url, path) for path in ignore],
            client=client,
            limit=asyncio.BoundedSemaphore(max_tasks),
        )

        state = State(todo=set(), busy=set(), done=set(), tasks=set())

        fut = asyncio.ensure_future(add_url(root_url, "", config, state))
        state.tasks.add(fut)

        await asyncio.sleep(0.1)
        while state.busy:
            await asyncio.sleep(0.5)

    urls = sorted(
        replace_root(url, host) if host is not None else url for url in state.done
    )

    if check:
        return 0 if compare_xml(urls=urls, output=output) else 1

    write_xml(
        urls=urls, output=output,
    )
    return 0


async def add_url(url: str, parent_url: str, config: Config, state: State) -> None:
    url = urljoin(parent_url, url)
    url, _ = urldefrag(url)

    if (
        not url.startswith(config.root_url)
        or any(url.startswith(prefix) for prefix in config.ignore)
        or url in state.todo
        or url in state.busy
        or url in state.done
    ):
        return

    state.todo.add(url)
    fut = asyncio.ensure_future(process(url, config, state))
    fut.add_done_callback(state.tasks.remove)
    state.tasks.add(fut)


async def process(url: str, config: Config, state: State) -> None:
    async with config.limit:
        state.todo.remove(url)
        state.busy.add(url)

        try:
            r = await config.client.get(url)
        except BaseException:
            traceback.print_exc()
            return
        else:
            if r.status_code == 200 and "text/html" in r.headers.get("content-type"):
                hrefs = re.findall(r'(?i)href=["\']?([^\s"\'<>]+)', r.text)
                for href in hrefs:
                    fut = asyncio.ensure_future(add_url(href, url, config, state))
                    fut.add_done_callback(state.tasks.remove)
                    state.tasks.add(fut)

            state.done.add(url)
        finally:
            state.busy.remove(url)


def make_xml(urls: Sequence[str]) -> str:
    content = "\n".join(
        [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 '
            'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">',
            *(
                f"  <url><loc>{url}</loc><changefreq>daily</changefreq></url>"
                for url in urls
            ),
            "</urlset>",
        ]
    )

    return f"{content}\n"


def compare_xml(urls: Sequence[str], output: str) -> bool:
    with open(output) as f:  # type: Any
        content = f.read()
        return content == make_xml(urls)


def write_xml(urls: Sequence[str], output: str) -> None:
    with open(output, mode="w") as f:  # type: Any
        f.write(make_xml(urls))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("root_url")
    parser.add_argument("-O", "--output", default="sitemap.xml")
    parser.add_argument("-H", "--host")
    parser.add_argument("-I", "--ignore", action="append")
    parser.add_argument("-C", "--concurrency", type=int, default=100)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--asgi", action="store_true")
    args = parser.parse_args()

    if not args.host:
        args.host = args.root_url

    async def main() -> int:
        exit_stack = AsyncExitStack()

        if args.asgi:
            try:
                from asgi_lifespan import LifespanManager
            except ImportError:
                print("`asgi-lifespan` must be installed to use --asgi")
                return 1

            # Treat `root_url` as path.to.module:app
            module, name = args.root_url.split(":")
            mod = importlib.import_module(module)
            app = getattr(mod, name, None)
            assert app is not None
            await exit_stack.enter_async_context(LifespanManager(app))
            client = httpx.AsyncClient(app=app)
            args.root_url = "http://localhost:8000"
        else:
            client = httpx.AsyncClient()

        return await crawl(
            root_url=args.root_url,
            output=args.output,
            host=args.host,
            ignore=args.ignore,
            max_tasks=args.concurrency,
            client=client,
            check=args.check,
        )

    sys.exit(asyncio.run(main()))
