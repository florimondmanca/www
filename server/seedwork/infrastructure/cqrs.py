from typing import TypeVar

from ..domain.cqrs import MessageBus, Query

T = TypeVar("T")


class AsyncBus(MessageBus):
    def __init__(self, query_handlers: dict) -> None:
        self._query_handlers = query_handlers

    async def execute(self, query: Query[T]) -> T:
        try:
            handler = self._query_handlers[type(query)]
        except KeyError:  # pragma: no cover
            raise NotImplementedError(f"No handler for {query=}")

        return await handler(query)
