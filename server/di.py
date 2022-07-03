from typing import Type, TypeVar

import punq

from .domain.repositories import PageRepository
from .infrastructure.repositories import InMemoryPageRepository

T = TypeVar("T")


def _configure(container: punq.Container) -> None:
    container.register(PageRepository, instance=InMemoryPageRepository())


_container = punq.Container()
_bootstrapped = False


def bootstrap() -> None:
    global _bootstrapped
    _configure(_container)
    _bootstrapped = True


def resolve(type_: Type[T]) -> T:
    assert _bootstrapped, "DI not initialized: call bootstrap()"
    return _container.resolve(type_)
