from typing import Generic, TypeVar

T = TypeVar("T")


class Query(Generic[T]):
    pass


class MessageBus:
    async def execute(self, query: Query[T]) -> T:
        raise NotImplementedError  # pragma: no cover
