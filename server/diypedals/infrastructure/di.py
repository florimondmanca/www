from typing import Callable, Type, TypeVar

import punq

T = TypeVar("T")


class Container:
    def __init__(self, configure: Callable[["Container"], None]) -> None:
        self._impl = punq.Container()
        self._configure = configure
        self._is_configured = False

    def register(self, type_: Type[T], *, instance: T) -> None:
        self._impl.register(type_, instance=instance)

    def bootstrap(self) -> None:
        if self._is_configured:
            return  # pragma: no cover

        self._configure(self)
        self._is_configured = True

    def resolve(self, type_: Type[T]) -> T:
        assert self._is_configured, "DI not configured: call bootstrap()"
        return self._impl.resolve(type_)
