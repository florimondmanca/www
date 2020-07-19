---
published: true
title: "A practical usage of ChainMap in Python"
description: "ChainMap in a nutshell: treat multiple dictionaries as one, unlock Python superpowers."
date: "2018-07-25"
legacy_url: "/a-practical-usage-of-chainmap-in-python"
tags:
  - python
  - devtips
---

The collections module from Python's standard library contains many useful data structures designed for performance. Famous ones include `namedtuple` or `Counter`.

Today, we'll take a look at the lesser known **ChainMap** and go through practical usage examples. By going through concrete examples, I hope to give you a hint on how you may benefit from using ChainMap in your more advanced Python work.

**Disclaimer**: this post is about a rather advanced feature of Python. If you're just getting started, hang tight!

## What is ChainMap?

**ChainMap** is a data structure provided by the Python standard library that allows you to treat multiple dictionnaries as one.

The [official documentation](https://docs.python.org/3/library/collections.html#collections.ChainMap) on ChainMap reads:

> A ChainMap groups multiple dicts or other mappings together to create a single, updateable view. […] Lookups search the underlying mappings successively until a key is found. […] If one of the underlying mappings gets updated, those changes will be reflected in ChainMap. […] All of the usual dictionary methods are supported.

In other words: **a ChainMap is an updatable view over multiple dicts, and it behaves just like a normal dict.**

Since you've probably never heard of ChainMap before, you may think that the use cases of ChainMap are quite specific. And to be frank, you'd be right.

However, the use cases I know of include:

- Searching through multiple dictionnaries
- Providing a chain of default values
- Performance-critical applications that frequently compute subsets of a dictionnary

We'll go through two examples to illustrate.

_Note: these two examples are greatly inspired by a post written by Mike Driscoll on [The Mouse vs. The Python](https://www.blog.pythonlibrary.org/2016/03/29/python-201-what-is-a-chainmap/). I have adapted them for my purpose but be sure to check out his post for another view on ChainMap!_

## Example: the shopping inventory

As a first example of using ChainMap, let's consider an inventory of shopping items. Our inventory may contain toys, computers or even clothing. All of these items have a price so we'll store our items in name-price mappings.

```python
>>> toys = {'Blocks': 30, 'Monopoly': 20}
>>> computers = {'iMac': 1000, 'Chromebook': 800, 'PC': 400}
>>> clothing = {'Jeans': 40, 'T-Shirt': 10}
```

We can now use ChainMap to build a single view over these disparate collections:

```python
>>> from collections import ChainMap
>>> inventory = ChainMap(toys, computers, clothing)
```

This allows us to query the inventory **as if it was a single dictionnary**:

```python
>>> inventory['Monopoly']
20
```

As the official docs state, ChainMap supports all the usual dictionnary methods. We can use `.get()` to search for items that may not be present, or remove items using `.pop()`.

```python
>>> inventory.get('Mario Bros.')
None
>>> inventory.pop('Blocks')
200
>>> inventory['Blocks']  # KeyError: 'Blocks'
```

If we now add a toy to the `toys` dictionnary, it will also be made available in the inventory. This is the **updatable** aspect of a ChainMap.

```python
>>> toys['Nintendo'] = 200
>>> inventory['Nintendo']
200
```

Oh and ChainMap has a pretty string representation as well:

```python
>>> str(inventory)
ChainMap({'Monopoly': 20, 'Nintendo': 200}, {'iMac': 1000, 'Chromebook': 800, 'PC': 400}, {'Jeans': 40, 'T-Shirt': 10})
```

A nice feature is that while in our example `toys`, `computers` and `clothing` are all in the same context (the interpreter), they could come from totally different modules or packages. This is because ChainMap stores the underlying dictionnaries **by reference**.

This first example was about using ChainMap to search through multiple dictionnaries at once.

In fact, when building a ChainMap, what we do is effectively building a _chain of dictionnaries_. When looking up an item in the inventory, toys are looked up first, then computers and finally clothing.

![A ChainMap is really just… a chain of mappings!](https://florimondmanca-personal-website.s3.amazonaws.com/media/markdownx/d6d63ed6-2ee4-432a-81fa-586937e6ee04.png)

Actually, another task where ChainMap shines is at **maintaining a chain of defaults**.

We'll take the example of a command line application to illustrate what this means.

## Example: CLI configuration

Let's face it, managing configuration of command lines applications can be difficult.

Configuration is drawn from multiple sources: command line arguments, environment variables, local files, etc.

We generally implement a notion of **priority**: if `A` and `B` both define parameter `P`, `A`'s value for `P` will be used because it has priority over `B`.

For example, we may want to use command line arguments over environment variables if the former were passed.

How can we easily manage priority of configuration sources?

One answer would be to store all configuration sources in a ChainMap.

Because **a lookup in a ChainMap is performed on each underlying mapping successively** (in the order they were passed to the constructor), we can easily achieve the prioritization we were looking for.

Below is a simple command line application. There, a `debug` parameter is drawn from either command line arguments, environment variables or hard-coded defaults:

```python
# cli.py
import argparse
import os
from collections import ChainMap

defaults = {"debug": False}

parser = argparse.ArgumentParser()
parser.add_argument("--debug")
args = parser.parse_args()
cli_args = {key: value for key, value in vars(args).items() if value}

config = ChainMap(cli_args, os.environ, defaults)

print(config.get("debug"))
```

When executing the script, we can check that `debug` is first looked up in the command line arguments, then the environment variables and finally the defaults as a last resort:

```bash
$ python cli.py
False
$ python cli.py --debug 1
1
$ export debug=True
$ python cli.py
True
$ python cli.py --debug yes
yes
```

Neat, right?

## Why should I care?

To be honest, ChainMap is one of those Python features that you can probably afford to ignore.

There are also alternatives to using ChainMap. For example, using an update-loop — i.e. creating a dict and `.update()`-ing it with your dictionnaries — may do the trick. But this only works if you don't need to keep track of the origin of the items, as was the case in our multi-source CLI configuration example.

**However, ChainMap can make your life much easier and your code much more elegant when you know it exists.**

In fact, the very first time I used ChainMap was just a week ago. Why not before? I simply never had the use.

I used it because I needed to frequently compute a subset of a dictionnary (based on an attribute of the value), which was costly. I instead needed to achieve **constant-time lookups** to meet performance requirements.

I decided to split the dictionnary into two distinct dicts and perform the branching at insert time. I then used ChainMap to group these two dicts together. This way, I could keep the initial view on the single dictionnary — but also lookup each separate dictionnary in constant time!

---

## Wrap up

To sum up, we have seen together what ChainMap is, some concrete usage examples, and how it can be used in real-life, performance-critical applications.

If you want to know more about Python's high-performance data containers, be sure to check out the rest of the fantastic [collections module](https://docs.python.org/3/library/collections.html) from Python's standard library. 💻