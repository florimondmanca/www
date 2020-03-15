from . import resources
from .loader import load_pages


async def init() -> None:
    resources.index.pages = await load_pages()


async def reload() -> None:
    await init()
