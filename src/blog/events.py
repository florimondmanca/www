from .resources import index
from .utils import load_index


async def on_startup() -> None:
    await load_index(index)


async def on_shutdown() -> None:
    index.clear()
