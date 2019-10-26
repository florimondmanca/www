import pathlib

from starlette.staticfiles import StaticFiles
from starlette.types import Receive, Scope, Send

HERE = pathlib.Path(__file__).parent
BUILD_DIR = HERE / "site" / ".vuepress" / "dist"
assert (
    BUILD_DIR.exists()
), "Blog site hasn't been built yet. HINT: run `$ scripts/build`."

static = StaticFiles(directory=str(BUILD_DIR))


def normalize_path(path: str) -> str:
    # VuePress outputs each page into a folder containing a single "index.html" file.
    if path.endswith("/"):
        return f"{path}index.html"
    elif not path.endswith("/index.html"):
        return f"{path}/index.html"
    return path


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    scope["path"] = normalize_path(scope["path"])
    await static(scope, receive, send)
