from .loader import load_pages
from .resources import index


async def load() -> None:
    index.pages = await load_pages()
