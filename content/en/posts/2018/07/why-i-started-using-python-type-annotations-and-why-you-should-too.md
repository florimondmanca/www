---
title: "Why I started using Python type annotations – and why you should too"
description: "Type hints add optional static typing to Python 3.5+, and I love them. I now use annotated variables throughout my projects."
date: "2018-07-27"
legacy_url: "/why-i-started-using-python-type-annotations-and-why-you-should-too"
category: essays
tags:
  - python
image: "/static/img/articles/python-type-annotations.jpg"
image_thumbnail: __auto__
image_caption: "Code snippet, carbon.now.sh"
---

When Python 3.6 was released back in december 2016, I was excited at some of the new features it provided. Among them, [f-strings](https://www.python.org/dev/peps/pep-0498/?) were quite a highlight for me (if you don't use them yet, start today!).

Some time after I upgraded my stack to use Python 3.6, I heard about type annotations thanks to [a video from Dan Bader](https://www.youtube.com/watch?v=2xWhaALHTvU). He explained what type annotations were and why he found them useful.

Although they were introduced in Python 3.5 (back in 2015), I have only started using type annotations a few months ago.

**Because they help me and my peers write more readable, elegant and arguably plain better code, I now use type annotations in all my projects.**

I figured now was a good time to also share my experience!

## Static typing in Python?! Nope, not for me

When I first heard of type annotations, I was not convinced. I thought type annotations were some sort of hack of the Python language itself.

The idea of specifying types while using a dynamically typed language seemed plain odd to me, given that I had been doing great for years with Python's dynamic nature.

At the time, I was perfectly fine with writing code like:

```python
def set_pos(self, pos):
    self.x = pos[0]
    self.y = pos[1]
```

What should `pos` contain? Well, that's obvious — just look at the code and you can immediately tell it should be a tuple containing two numbers (_what kind of number? Integers? Floats?_).

I also learned that type annotations were actually not used by Python's runtime at all. They were completely _ignored_. So I thought — what use if it has no influence on the execution of the code I write?

I really couldn't grasp all the growing fuss about introducing static typing into Python.

## Until you start working with other devs

I began working as a software engineering intern at [ComplyAdvantage](https://complyadvantage.com) in March 2018. I have been lucky enough that this startup treats their interns with the same level of trust and responsibilities as their actual employees. As such, I have been working on challenging, real-life projects since then.

In fact, it's been my very first work experience as a developer. I never had to read much of other people's code before, and they never really had to read mine. And you guessed it — Python is all the rage at ComplyAdvantage.

One of the first pieces of code I read was written by my mentor. He's one of those guys with a strong Java background who also picked up Python for their job — and are doing great at it. Coming from the world of statically typed languages, he was a strong advocate of Python type annotations, and he used them all over his code. When I asked why, he roughly said to me:

> It's just clearer for everyone. Type annotations tell other people what your code's inputs and outputs are — and they don't even have to do the effort of asking.

The fact that this statement focuses so much on _other people_ struck me.

He was basically saying that **one uses type annotations to help others understand their code more easily.**

## Readability counts

Think about it for a moment. When you work on a project, the code you write may make a lot of sense to you right now. You don't feel the need to document it too much.

But other people (including the 6-months-from-now version of yourself) will in the future have to **read your code and understand what it all means**. As I learnt from a colleague, they'll need to answer at least **three basic questions**:

1. What does this piece of code take as an input?
2. How does it process the input?
3. What does it produce as an output?

As I was reading more and more of other people's code — including complex legacy code — I realized that type annotations were actually **extremely useful**. They were helping me to answer questions 1/ and 3/ **at light speed**. (Question 2/ could be answered just as easily with meaningful function names.)

## Let's play a quick game

I have written below a function whose body has been hidden. **Can you tell me what it does?**

```python
def concat(a, b):
    ...
```

Here's my take — from the function name, I would say that `concat()` takes two lists (_or tuples?_) and concatenates them to return a single list containing the elements of `a` and `b`.

Obvious, right? **Not really.**

There are actually other possibilities. What if `concat()` actually simply concatenates two strings, for example?

The thing is — **we don't really understand what `concat()` does because we cannot answer all three questions from above.** Only can we roughly answer question 2/ by: "it does some sort of concatenation".

Now, let's add **type annotations** to `concat()`:

```python
def concat(a: int, b: int) -> str:
    ...
```

Ah-ha! We were actually wrong in both our guesses. It seems `concat()` takes two integers and outputs a string.

So I would now say — it takes two integers as an input, turns them into their string representation, concatenates them and returns the result.

And that's exactly what it does:

```python
def concat(a: int, b: int) -> str:
    return str(a) + str(b)
```

This example shows you that **knowing the inputs and outputs is crucial to understanding a piece of code**. And type annotations help you let your readers know almost instantly.

## There used to be a workaround

Reflecting back on my experience, it turns out I already knew this — way before I started using type annotations — and probably so did you.

I always loved writing clean code and documenting it was well as I could. I believe it is good discipline to add a docstring on all your functions and classes to explain what they do (_functionality_) and why they even exist (_purpose_).

Here is an actual code snippet from a personal project I worked on a few years ago:

```python
def randrange(a, b, size=1):
    """Return random numbers between a and b.

    Parameters
    ----------
    a : float
        Lower bound.
    b : float
        Upper bound.
    size : int, optional
        Number of numbers to return. Defaults to 1.

    Returns
    -------
    ns : list of float
    """
    ...
```

_Let's see… a docstring that describes parameters, along with their types, and the output value along with its type…_

Woah.

In a sense, **I was already using type annotations — via docstrings.**

Don't get me wrong: **documenting your code with docstrings is great and useful** when the component has a lot of logic. There are standard formats (I used the [NumPy doc format](http://numpydoc.readthedocs.io/en/latest/format.html) above) which are helpful as they ensure documentation conventions and can be interpreted by some IDEs as well.

However **for simple functions**, using a full-blown docstring just to describe arguments and return values **sometimes felt like a workaround** — for the fact that Python did not offer any notion of type hinting whatsoever (_or so I thought_).

**Type annotations can sometimes replace a docstring altogether** as they are — in my opinion — a very clean and simple way of documenting inputs and outputs. In the end, **your code is easier to read both for you and your fellow developers.**

## But wait! There's more

Type annotations were added to Python 3.5 along with [the typing module](https://docs.python.org/3/library/typing.html).

This module provides ways to annotate all kinds of types (like lists, dictionnaries, functions or generators) and even supports nesting, generics and the ability to define your own custom types.

I won't dive into the details of the `typing` module, but I just wanted to share something I discovered not so long ago: type annotations can be used to generate code.

I'll take the example of `namedtuple`. This is a data structure from the `collections` module — just like ChainMap which we already covered in [A practical usage of ChainMap in Python](/blog/articles/2018/07/a-practical-usage-of-chainmap-in-python).

What `namedtuple` does is generate a class whose instances behave like tuples (they are immutable) but allow attribute access via dot notation.

A typical usage of `namedtuple` is the following:

```python
from collections import namedtuple

Point = namedtuple("Point", "x y")
point = Point(x=1, y=5)
print(point.x)  # 1
```

If we remember what we said about the importance of documenting inputs and outputs, there's something missing here. **We don't know what the types of `x` and `y` are**.

It turns out that the `typing` module has an equivalent of `namedtuple` called `NamedTuple` which allows you to use type annotations.

Let's redefine the `Point` class with `NamedTuple`:

```python
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


point = Point(x=4, y=0)
print(point.x)  # 4
```

**I \*love\* this.** Beautiful, clean and explicit Python code.

Note that the usage of `Point` is exactly the same as before, except we now benefit from more readable code — and our IDEs and editors can help us detect potential type errors as well thanks to static checkers such as [MyPy](http://mypy-lang.org) (and their various [integrations](https://atom.io/packages/linter-mypy)).

There are many more exciting things you can do with type annotations, especially since they are now a core part of the Python language.

For instance, Python 3.7 has introduced [data classes](https://www.python.org/dev/peps/pep-0557/#id7), an exciting new way of generating classes for simple yet efficient data storage. However, they would be worth their own blog post entirely, so I'll keep them for later.

## What about philosophy?

Python was designed as a dynamic programming language, and we're now introducing static typing to it. At this point, some may wonder:

How can this fit the language's philosophy?

**Have the Python core developers just realized that dynamic typing was a mistake?**

Well, not really. Try searching for `python philosophy` on Google and here's what you'll get:

[PEP 20 - The Zen of Python](https://www.python.org/dev/peps/pep-0020/)

The Zen of Python drives the philosophy of the langage as a whole.

In my opinion, **type annotations are 100% aligned with Python's philosophy**. Here are some aphorisms they embody perfectly.

### **Explicit is better than implicit.**

This is basically the reason why type annotations were invented in the first place. Just compare:

```python
def process(data):
    do_stuff(data)
```

and:

```python
from typing import List, Tuple


def process(data: List[Tuple[int, str]]):
    do_stuff(data)
```

### **Simple is better than complex.**

In simple cases, using type hinting is way simpler than resorting to full-blown docstrings.

### **Readability counts.**

Well, we've already discussed this one. 😉

### **There should be one — and preferably only one — obvious way to do it.**

This is implemented with the strict (yet simple) syntax for type annotations. They are the go-to if you want to document and support static types in Python!

And lastly…

## Now is better than never

To me, **type annotations were a game changer**:

- They improved the way I write code.
- By providing a standard way to document inputs and outputs, they help you _and other people_ understand and reason about code much more easily.
- They also enable new ways of writing code in a cleaner and more concise way.

If you're not using type annotations yet: start now! There is [a lot](https://www.youtube.com/watch?v=7ZbwZgrXnwY) of [great content](https://www.youtube.com/watch?v=QCGwDOk-pIs) about them [out there](https://www.youtube.com/channel/UCI0vQvr9aFn27yR6Ej6n5UA) to get started.

If you're already using — and hopefully digging — type annotations: help spread the love! Write about it, share it with your colleagues and fellow developers.

Type annotations are incredible and now a core piece of the Python language. Let's use more of those! 💻
