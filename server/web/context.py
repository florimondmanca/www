from ..di import resolve
from ..domain.repositories import CategoryRepository


async def get_navbar_context() -> dict:
    category_repository = resolve(CategoryRepository)

    return {
        "categories": await category_repository.find_all(),
    }
