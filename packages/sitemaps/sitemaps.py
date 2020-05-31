import importlib
import re
import sys
from contextlib import AsyncExitStack
from functools import partial
from typing import Iterator, NamedTuple, Sequence, Set
from urllib.parse import urldefrag, urljoin, urlsplit

import anyio
import httpx


class Config(NamedTuple):
    root_url: str
    ignore: Sequence[str]
    client: httpx.AsyncClient
    limit: anyio.CapacityLimiter
    tg: anyio.TaskGroup


class State(NamedTuple):
    discovered_urls: Set[str]
    results: Set[str]


async def crawl(
    root_url: str,
    host: str = None,
    ignore: Sequence[str] = (),
    max_tasks: int = 100,
    client: httpx.AsyncClient = None,
) -> Sequence[str]:
    client = httpx.AsyncClient() if client is None else client

    async with client, anyio.create_task_group() as tg:
        config = Config(
            root_url=root_url,
            ignore=[urljoin(root_url, path) for path in ignore],
            client=client,
            limit=anyio.create_capacity_limiter(max_tasks),
            tg=tg,
        )
        state = State(discovered_urls=set(), results=set())
        await enqueue(root_url, parent_url="", config=config, state=state)

    return sorted(
        (replace_root(url, host) if host is not None else url) for url in state.results
    )


async def enqueue(url: str, parent_url: str, config: Config, state: State) -> None:
    url = urljoin(parent_url, url)
    url, _ = urldefrag(url)

    if (
        not url.startswith(config.root_url)
        or any(url.startswith(prefix) for prefix in config.ignore)
        or url in state.discovered_urls
    ):
        return

    state.discovered_urls.add(url)
    await config.tg.spawn(partial(process, url, config=config, state=state))


def replace_root(url: str, root_url: str) -> str:
    return urljoin(root_url, urlsplit(url).path)


def is_ok_html(response: httpx.Response) -> bool:
    content_type = response.headers.get("content-type", "")
    return response.status_code == 200 and "text/html" in content_type


async def process(url: str, config: Config, state: State) -> None:
    async with config.limit:
        response = await config.client.get(url)

        if "text/html" in response.headers.get("content-type", ""):
            hrefs = re.findall(r'(?i)href=["\']?([^\s"\'<>]+)', response.text)
            for href in hrefs:
                await config.tg.spawn(
                    partial(enqueue, href, url, config=config, state=state)
                )

        state.results.add(url)


def make_xml(urls: Sequence[str]) -> str:
    def lines() -> Iterator[str]:
        yield '<?xml version="1.0" encoding="utf-8"?>'
        yield (
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 '
            'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
        )
        for url in urls:
            yield f"  <url><loc>{url}</loc><changefreq>daily</changefreq></url>"
        yield "</urlset>"

    content = "\n".join(lines())
    return f"{content}\n"


async def compare_xml(urls: Sequence[str], output: str) -> bool:
    async with await anyio.aopen(output) as f:
        content = await f.read()
        return content == make_xml(urls)


async def write_xml(urls: Sequence[str], output: str) -> None:
    async with await anyio.aopen(output, mode="w") as f:
        await f.write(make_xml(urls))


async def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("-O", "--output", default="sitemap.xml")
    parser.add_argument("-H", "--host")
    parser.add_argument("-I", "--ignore", action="append")
    parser.add_argument("-C", "--concurrency", type=int, default=100)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--asgi", action="store_true")
    args = parser.parse_args()

    if not args.host:
        args.host = args.target

    async with AsyncExitStack() as exit_stack:
        if args.asgi:
            try:
                from asgi_lifespan import LifespanManager
            except ImportError:
                print("`asgi-lifespan` must be installed to use --asgi")
                return 1

            # Treat `target` as 'path.to.module:app'.
            module, name = args.target.split(":")
            mod = importlib.import_module(module)
            app = getattr(mod, name, None)
            assert app is not None
            await exit_stack.enter_async_context(LifespanManager(app))

            client = httpx.AsyncClient(app=app)
            root_url = "http://localhost:8000"
        else:
            # Treat `target` as an URL.
            client = httpx.AsyncClient()
            root_url = args.target

        urls = await crawl(
            root_url=root_url,
            host=args.host,
            ignore=args.ignore,
            max_tasks=args.concurrency,
            client=client,
        )

    if args.check:
        return 0 if await compare_xml(urls, args.output) else 1

    await write_xml(urls, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(anyio.run(main))
