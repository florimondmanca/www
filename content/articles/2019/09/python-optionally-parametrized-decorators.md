---
published: true
title: "How to write optionally callable parametrized decorators in Python"
description: "A memo on implementing parametrized decorators whose default behavior doesn't require empty parentheses."
date: "2019-09-28"
legacy_url: "/python-optionally-parametrized-decorators"
tags:
  - python
  - tutorial
  - devtips
image: "/static/img/articles/optionally-parametrized-decorators.png"
image_caption: "A code snippet of what we're aiming to achieve."
---

This blog post is a memo to myself, and to anyone who wants to know (or keeps forgetting like I do 😬) how to implement Python parametrized decorators without needing to call them in the no-arguments use case.

Not sure what I'm talking about? An example of this very handy pattern can be found in [pytest fixtures](https://docs.pytest.org/en/latest/fixture.html):

```python
import pytest

@pytest.fixture  # No need to write '@pytest.fixture()'
def app():
    ...

@pytest.fixture(scope="session")
def server():
    ...
```

## Concrete example

Let's write an `@logged` decorator for numeric functions.

It accepts an optional `decimals` argument to round the result of the computation to a certain number of digits. If `decimals` is not given, we shouldn't round at all.

So, possible invokations should be:

- `@logged()`
- `@logged(decimals=2)`
- `@logged` (Equivalent of `@logged()`) — implementing this is the goal of this blog post.

Cutting to the chase, here's the annotated solution:

```python
import functools
import typing

def logged(func: typing.Callable = None, decimals: int = None) -> typing.Callable:
    if func is None:
        print(f"Called with decimals={decimals}")
        return functools.partial(logged, decimals=decimals)

    print(f"Called without parameters, func={func}.")

    @functools.wraps(func)
    def decorated(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        print(f"{func.__name__} called with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logged_result = result if decimals is None else round(result, decimals)
        print(f"Result: {logged_result}")
        return result

    return decorated
```

If we run the following script:

```python
@logged
def add(x: float, y: float) -> float:
    return x + y

@logged(decimals=2)
def mult(x: float, y: float) -> float:
    return x * y

add(2, 2)
mult(3, 4)
```

We get the following output:

```console
Called without parameters, func=<function add at 0x10d8d8b70>.
Called with decimals=2
Called without parameters, func=<function mult at 0x10db18a60>.
add called with args=(2, 2), kwargs={}
Result: 4
mult called with args=(3, 4), kwargs={}
Result: 12
```

Boom.

## Generic implementation

This 100% generic implementation is stripped of any comments and debug outputs. Just copy-paste it somewhere and adapt it to your needs.

```python
import functools
import typing

def decorate(func: typing.Callable = None, **options: typing.Any) -> typing.Callable:
    if func is None:
        return functools.partial(decorate, **options)

    @functools.wraps(func)
    def decorated(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return func(*args, **kwargs)

    return decorated
```

That's it! Go add this extra juice to your decorator-based APIs. 🚀
