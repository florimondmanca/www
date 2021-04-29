---
title: "Reconciling Dataclasses And Properties In Python"
description: "I love Python dataclasses, but combining them with properties is not obvious. This is a problem solving report — and a practical introduction to dataclasses!"
date: "2018-10-10"
legacy_url: "/reconciling-dataclasses-and-properties-in-python"
category: tutorials
tags:
  - python
image: "/static/img/articles/dataclasses-properties.jpg"
image_caption: "Two black-and-white birds. @wwwynand, unsplash.com"
---

_If you can't wait for the TL;DR, jump to "Lessons Learned" at the end of this article._

I've been playing around with Python 3.7's [dataclasses](https://docs.python.org/3/library/dataclasses.html) — and so far they've been super awesome. For the most part, they're quite intuitive and easy to use and customize.

Yet, there's one thing I've been struggling with and couldn't find online help for, which is **implementing Python properties on dataclasses**. And chances are — I am not alone.

That's why I decided to solve the problem once and for all. I wanted to figure out **how to reconcile dataclasses and properties**.

So I sat down before my computer, fired up an interpreter and wrote down my thought process as I made my way towards a solution. After a night of trial and error and some wording enhancements, the result is this very blog post!

As a pleasant side effect, you'll get to **see many features of dataclasses in action**. I'll start with a quick overview of dataclasses, and we'll get to the code right after that.

Of course, you'll find all the code supporting this post on [GitHub](https://github.com/florimondmanca/dataclasses-properties).

## Dataclasses: a 10,000-ft overview

Dataclasses are, simply put, **classes made to hold data**. Their specification in [PEP-557](https://www.python.org/dev/peps/pep-0557) was motivated by the fact that a lot of classes we write are merely used as editable data containers. When that happens, we spend time writing boilerplate code which most often results in an ugly `__init__()` method with tons of arguments and just as many lines for storing them as attributes — not to speak about handling [default arguments](https://blog.florimondmanca.com/python-mutable-defaults-are-the-source-of-all-evil)…

![Dataclasses, featuring Raymond Hettinger.](/static/img/dataclasses-properties-hettinger.jpg)

And there is! The answer is: **dataclasses**. 🎉

Python implements dataclasses in the well-named [dataclasses](https://docs.python.org/3/library/dataclasses.html) module, whose superstar is the `@dataclass` decorator. This decorator is really just a **code generator**. It takes advantage of Python's type annotations (if you still don't use them, [you really should](https://blog.florimondmanca.com/why-i-started-using-python-type-annotations-and-why-you-should-too)) to **automatically generate boilerplate code** you'd have to mechanically type yourself otherwise.

As a point of comparison, here's how you would create a `Vehicle` class with a `wheels` attribute using a regular class declaration:

```python
class Vehicle:
    def __init__(self, wheels: int):
        self.wheels = wheels
```

Nothing fancy, really. Now, the `@dataclass` version:

```python
# 0_initial.py
from dataclasses import dataclass


@dataclass
class Vehicle:
    wheels: int
```

Believe it or not — these two code snippets are strictly equivalent! It's actually a win, because beyond `__init__()`, `@dataclass` generates a bunch of extra stuff for free, including a handsome `__repr__()`:

```python
>>> car = Vehicle(wheels=4)
>>> car
Vehicle(wheels=4)
```

In short, dataclasses are a simple, elegant, Pythonic way of creating classes that hold data. 🐍

But…

## The problem

I sometimes resort to the `@property` decorator to implement specific logic when getting/setting an attribute. That's really just the Pythonic way of implementing getters and setters.

Building upon the previous `Vehicle` class, I would make the `wheels` attribute private and put an `@property` on top of it:

```python
class Vehicle:
    def __init__(self, wheels: int):
        self._wheels = wheels
        # note the underscore — it's now private! 👻

    @property
    def wheels(self) -> int:
        print("getting wheels")
        return self._wheels

    @wheels.setter
    def wheels(self, wheels: int):
        print("setting wheels to", wheels)
        self._wheels = wheels
```

Here's what it looks like:

```python
>>> car = Vehicle(wheels=4)
>>> car.wheels = 3
setting wheels to 3
>>> car.wheels
getting wheels
3
>>>
```

Now the question is — **how can I implement such a property on a dataclass?**

## Wait, so _this_ is the problem?

You may think this to be a trivial question. Mind you, **it is not trivial**.

Dataclasses generate the `__init__()` method for you — and that's great. They even provide a `__post_init__()` hook method in case you want to do some more initialization (see [Post-init processing](https://docs.python.org/3/library/dataclasses.html#post-init-processing)).

However, this means you cannot do the same trick as with normal classes, i.e. storing a public-looking argument (e.g. `wheels`) into a private attribute (`_wheels`) that you'll build an `@property` out of.

That's where the problem comes from. And to be honest, it gave me a bit of a headache.

Because I think the problem solving was interesting, I'll take you through 5 consecutive attempts to correctly implement that property on a dataclass version of the `Vehicle` class.

## Attempt 1: declaring a private field

First, let's keep things simple. We want to store `wheels` in a private field and use it in the `@property`, right? So why not simply declare a `_wheels` field on the dataclass?

```python
# 1_private_field.py
from dataclasses import dataclass


@dataclass
class Vehicle:
    _wheels: int

    # wheels @property as before
```

Unfortunately, this won't work — otherwise this blog post wouldn't be of much use! 😙

The reason why is because the constructor now expects a `_wheels` argument instead of `wheels`.

```python
>>> car = Vehicle(wheels=4)
Traceback (most recent call last)
<ipython-input-3-9c9de8fb1422> in <module>()
----> 1 car = Vehicle(wheels=4)
TypeError: __init__() got an unexpected keyword argument 'wheels'
```

To be fair, that's just `@dataclass` doing its job. Still, that's not what we want.

## Attempt 2: make use of `InitVar`

If you read through the documentation, you'll learn that `InitVar` allows you to implement [init-only variables](https://docs.python.org/3/library/dataclasses.html#init-only-variables). These variables can be passed to the constructor, but won't be stored in an attribute on the class. Instead, the variable is passed as an argument to `__post_init__()`.

Why not use this to create an init-only `wheels` variable and store that in a `_wheels` field? We just need to give the latter a default (e.g. `None`) so that it is not required by the constructor:

```python
# 2_initvar.py
from dataclasses import dataclass, InitVar


@dataclass
class Vehicle:

    wheels: InitVar[int]
    _wheels: int = None  # default given => not required in __init__()

    def __post_init__(self, wheels: int):
        self._wheels = wheels

    # wheels @property as before
```

Granted, `__init__()` now expects a `wheels` argument instead of `_wheels`, which is what we want.

However, `@dataclass` now generates other boilerplate code and magic methods using `_wheels`, which is problematic.

```python
>>> car = Vehicle(wheels=4)
setting wheels to 4
>>> car
Vehicle(_wheels=4)  # 😕
```

## Attempt 3: make use of `field()`

Digging deeper into the docs, I found that one could fine-tune the field generation behavior using the [field()](https://docs.python.org/3/library/dataclasses.html#dataclasses.field) function. You can pass it a `default` value and it accepts a `repr` argument to control whether the field should be included in the generated `__repr__()`. Here's how it looks when used on `_wheels`:

```python
# 3_field.py
from dataclasses import dataclass, field


@dataclass
class Vehicle:

    wheels: InitVar[int]
    _wheels: int = field(default=None, repr=False)

    # __post_init__() as before
    # wheels @property as before
```

Sweet — we don't have `_wheels` included in `__repr__()` anymore. But we still don't have `wheels` either!

```python
>>> car = Vehicle(wheels=4)
setting wheels to 4
>>> car
Vehicle()  # Where is `wheels=4`? 😕😕😕
```

## Attempt 4: make `wheels` a proper field

In the previous attempts, `wheels` was an `InitVar` — not a field. This time, let's declare it as a field in its own right. It will be possible to pass it in the constructor, and it should be included in `__repr__()` this time around.

The good thing is, the `@property` definition of `wheels` declared later in the class will not interfere with `@dataclass`'s generation process — _because it is not a type annotation_, which is what `@dataclass` relies on to generate the fields.

That might start to be a bit complicated, so let me show you some code. I'll reproduce the `@property` for `wheels` in full this time:

```python
# 4_wheels_field.py
from dataclasses import dataclass, field


@dataclass
class Vehicle:

    wheels: int  # Now a regular dataclass field

    # The rest just as before:

    _wheels: int = field(default=None, repr=False)

    def __post_init__(self):
        # Note: wheels is not passed as an argument
        # here anymore, because it is not an
        # `InitVar` anymore.
        self._wheels = self.wheels  # (1)

    @property
    def wheels(self) -> int:
        print("getting wheels")
        return self._wheels

    @wheels.setter
    def wheels(self, wheels: int):
        print("setting wheels to", wheels)
        self._wheels = wheels
```

It looks like we're getting there, aren't we?

Unfortunately, not quite. 😞 There's a catch in this implementation.

Indeed, you may think line `(1)` puts the value of `wheels` that was given to the constructor (and stored into `self.wheels`) into `_wheels`. For example, calling `Vehicle(wheels=4)` would result in having `_wheels == 4`. Sadly, that is not the case!

Here's why: when executing `__post_init__()`, `self.wheels` is the value returned by the `wheels` property's getter — _not_ the value initially stored during `__init__()`! And that getter returns `self._wheels`, which is `None` by default.

I know, it's getting all tangled up, but please bear with me:

```python
>>> car = Vehicle(wheels=4)
setting wheels to 4
getting wheels  # hint: this is (1) being executed
>>> print(car.wheels)
getting wheels
None  # nope, nothing in there…
```

If you think about it, what we're doing in (1) is just replacing `_wheels` with its own value. Quite useless, if you ask me. We would actually get the same result if we didn't even implement `__post_init__()`.

Duh! So what can we do? 😩

Fortunately, there's hope!

## Attempt 5: exclude `_wheels` from the constructor

_Let me warn you — this fifth and final attempt will work, and the reason why, which I'll explain in a minute, is outrageous._

At this point, you'd be right to feel sad — I felt sad myself. But fear not! There is one thing from the documentation that we haven't tried yet.

So far, the `_wheels` attribute has been declared using `field(default=None, repr=False)`. Using `default=None` here means that we are able to omit passing a value for `_wheels` in the constructor — it will be given the value of `None` during `__init__()`. However, it is still possible to give it a value in the constructor, and everything will work as expected:

```python
>>> car = Vehicle(wheels=4, _wheels=3)
setting wheels to 4
getting wheels
>>> car.wheels
getting wheels
3
```

Well, how about we find a way to remove the `_wheels` argument from the constructor? Will it solve our problem? (_Spoiler alert: it will._)

Guess what: `field()` accepts an `init` argument for that exact purpose. The docs on `field()` read:

> `init`: If true (the default), this field is included as a parameter to the generated `__init__` method.

Sounds trivial, right? Well, let's try using it on `_wheels` (I removed the `__post_init__()` hook because we previously showed that it was actually useless):

```python
# 5_init_false.py
from dataclasses import dataclass, field


@dataclass
class Vehicle:

    wheels: int
    _wheels: int = field(init=False, repr=False)

    @property
    def wheels(self) -> int:
        print("getting wheels")
        return self._wheels

    @wheels.setter
    def wheels(self, wheels: int):
        print("setting wheels to", wheels)
        self._wheels = wheels
```

Well, guess what? **This has just solved all of our problems**.

Because we used `init=False`, the constructor generated by `@dataclass` will not initialize `_wheels` at all.

**However**, it _will_ initialize `wheels` with the value passed to the constructor. If we could extract the generated code, one of the instructions in `__init__()` would look like this:

```python
self.wheels = wheels
```

Now, you tell me — what does this execute exactly?

Yep, that's right. It will execute the setter! 🙀

Look! We've actually been seeing the print statement in the setter since attempt 4!

```python
>>> car = Vehicle(wheels=4)
setting wheels to 4  # the `wheels` setter being called
```

Let me remind you of the code for that setter:

```python
@wheels.setter
def wheels(self, wheels: int):
    print("setting wheels to", wheels)
    self._wheels = wheels
```

It sets the value of `_wheels`!

As a result, the value for `wheels` passed in the constructor is put into `_wheels` — and nowhere else, because after the class has been generated, `wheels` only refers to the `@property`, not to a field on the dataclass.

If you think about it, this is exactly what we were doing when implementing the property on good ol' regular classes. Remember?

```python
class Vehicle:
    def __init__(self, wheels: int):
        self._wheels = wheels
        # This is equivalent to calling:
        # `self.wheels = wheels`
        # which *is* what the __init__() method
        # now generated by @dataclass actually does.
```

Caveat: **this approach only holds because the property's setter is implemented**. If we only implemented a getter (i.e. to make a read-only field), the `__init__()` method wouldn't be able to assign the attribute and would crash. This is intended behavior, though, because **dataclasses were designed to be editable data containers**. If you really need read-only fields, you shouldn't be resorting to dataclasses in the first place. Perhaps `NamedTuple`s would be a viable alternative — they are the read-only equivalent of dataclasses.

Anyway, long story short…

## Success!

We have successfully implemented properties on dataclasses. 🎉

![Memes will never let you down.](/static/img/dataclasses-properties-success.jpg)

To be honest, **it was surprisingly not easy**. We've been through five different attempts, navigating through the documentation and painstakingly coding our way towards dataclass properties.

So after all this hassle, can we at least derive **a quick recipe for implementing properties on dataclasses**?

The answer is: yes, we can. ✌️

## Lessons learned

Have you noticed a pattern between using an `@property` on a regular class vs. on a dataclass?

Look, here's the regular class version:

```python
class Vehicle:
    def __init__(self, wheels: int):
        self._wheels = wheels

    @property
    def wheels(self) -> int:
        return self._wheels

    @wheels.setter
    def wheels(self, wheels: int):
        self._wheels = wheels
```

And the dataclass version, using a diff syntax to highlight the differences:

```diff
+ from dataclasses import dataclass, field

+ @dataclass
  class Vehicle:

+     wheels: int
+     _wheels: int = field(init=False, repr=False)

-     def __init__(self, wheels: int):
-         self._wheels = wheels

      @property
      def wheels(self) -> int:
          return self._wheels

      @wheels.setter
      def wheels(self, wheels: int):
          self._wheels = wheels
```

Written in plain words, for you litterature freaks:

> **How to implement a property on a dataclass:**
>
> 1. Remove `__init__()`
> 2. Declare the property as a field
> 3. Add an associated private variable using `field(init=False, repr=False)`.

## Way to go!

If you managed to read up to here, congratulations! This blog post dealt with a highly specific and technical topic, yet I've had a lot of fun writing it and figuring out **how to implement dataclass properties**.

For those wondering — the series on Apache Kafka still goes on! I figured a small break never hurts, and I felt like it gave me the opportunity to write something spontaneous.

I hope you enjoyed this post and, as mentioned in introduction, you can find all the code on [GitHub](https://github.com/florimondmanca/dataclasses-properties). See you next time! 💻
