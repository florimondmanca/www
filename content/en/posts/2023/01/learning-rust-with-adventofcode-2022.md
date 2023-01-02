---
title: Learning Rust with Advent of Code
description: |
  I used Advent of Code 2022 to learn the basics of Rust. Here's a look at the benefits and shortcomings of this approach.
date: "2023-01-03"
category: retrospectives
tags:
  - til
image: "/static/img/articles/learning-with-advent-of-code.jpg"
image_thumbnail: __auto__
image_caption: "Elena Mozhvilo, unsplash.com"
---

I participated in [Advent of Code](https://adventofcode.com/) this December 2022. It was a lot of fun! My main motivation was to leverage the event to finally [learn Rust](https://www.rust-lang.org/learn) through actual practice.

In this post, I'd like to cover the benefits and shortcomings of using Advent of Code to learn Rust, and whether I would recommend Advent of Code to programming fellows eager to learn Rust. Spoiler: not sure. Why? Read on...

## What is Advent of Code (AoC)?

Advent of Code is an advent calendar of programming puzzles.

Each day comes with a new puzzle to solve. Puzzles generally take the form of finding a numeric output to a text input. For example, [day 2](https://adventofcode.com/2022/day/2) ("Rock Paper Scissors") was: find the total score of an input strategy given the scoring rules in the problem statement.

The problems are stated in the context of elves, monkeys and elephants going on adventures, which is kind of fun.

## How AoC helped me learn Rust

### AoC starts (very) small

The first major benefit of Advent of Code is that it gives **a good pretext** to learn Rust with enough structure. Overall, I'd say learning Rust has a certain barrier to it. It does some things in such a fundamentally different way to, say, dynamic interpreted languages (the background I came from). This means it takes time and effort just to _commit_ to learning it without stopping after a few hours of tinkering.

Next, what I really liked was how solving small programming problems allowed **discovering the language** instead of going all in and ending up feeling overwhelmed. Retrospectively, I think being effective with Rust takes requires some kind of paradigm shift, and that takes time. It's great to be able to start with very easy problems to cover a range of fundamental aspects of Rust without taking too much in at once.

For example, [day 1](https://github.com/florimondmanca/adventofcode2022/commit/67c5186c6930075eb13fbe64bf8d567b65815f1c) exposed me to:

* Basics of writing a Rust program (`src/main.rs` + `fn main() { ... }`)
* Basics of imports (`use std::fs`)
* Immutable (`let input = ...`) vs mutable (`let mut sum = 0`) variables
* Basics of functions (`fn run() -> ...`)
* Reading files
* Basics of error handling (`Result`, `Ok(...)`, the `?` suffix to propagate errors, and that `Box<dyn Error>` thingy which I'd develop an intuition about only much later in the journey)

All this is already quite a lot! The fact that day 1 was very easy (essentially, parse lines in a file as numbers and add them up) kept room for focusing on these first hands-on Rust concepts and techniques.

### AoC allows building up knowledge

Advent of Code does start with easy problems, but then difficulty ramps up gradually. This felt very suitable from a learning perspective.

In particular, there are some concepts that can only be sufficiently learnt through being exposed to a wide range of situations.

The memory management model (memory safety without a garbage collector thanks to ownership) is one that has rather fundamental implications on everything else we do in Rust. Starting small allows to build a practical intuition about concepts like ownership, borrowing, or lifetime on very simple problems at first, and then build up on that as days go by.

As the first couple of days went by, I was getting exposed to more and more concepts, features and techniques of Rust programming.

For example:

* [Day 2](https://github.com/florimondmanca/adventofcode2022/commit/5ee8553ad0655afd22223231cfc8aa3f10dbe539) exposed me to: enums, the notion of traits (`#[derive(Clone)]`), more functions, pattern matching, and the concept of moving (or — "oh, so I can't do `part1(input)` and then `part2(input)`?")
* [Day 3](https://github.com/florimondmanca/adventofcode2022/commit/865ecb8d286bb33b4678aab72a28f2bd60906f05) exposed me to: helper data structures (`Vec` for variable-length arrays, `HashSet` for sets), more text manipulation (e.g. `.chars()`), `.collect()` and its wild powers.

### Useful community resources

### The Rust tooling was a good companion

The community resources around AOC are great. Reddit threads allow to lookup hints to solutions if we’re blocked while not spoiling too much — although I had a hard time not stealing solutions when I had working code under my eyes, especially as I felt pressed to finish problems as quickly as possible. Which leads  us to the shortcomings of using AOC as a language learning tool…

## The shortcomings of AoC as a general language learning tool

### A somewhat repetitive solving model

The skeleton was always fairly similar: read an `input`, parse it by processing `input.lines()`, process the resulting data, compute the numeric answer and show it.

Problems end up somewhat repetitive. This is because of the “text in, number out” design of AOC. For example, 5 of the 24 problems involved parsing or modeling a 2D grid. Day 2(?) involved a 3D grid, which was refreshing.

### Brutal difficulty bumps (in the case of Rust)

The difficulty ladder depends on the language. For example, Rust happens to have a notable unfriendliness to self-referencing data structures, with a trees where nodes keep references to parents and/or children. For this reason, day 5 felt like a brutal step up, as the experience transitioned from playing with arithmetics to having to implement a somewhat advanced pattern to avoid issues with the borrow checker. The Rust community is friendly and I received helpful pointers and reassurance that yes, this is a difficult thing in Rust, but that was somewhat frustrating.

### A format that's fundamentally exclusive

AOC is impossible to complete if you have any kind of life on the side, or more generally if you’re not in a situation to dedicate 2 to 4 hours a day to a programming problem in a silent place. This means AOC is structurally reinforcing the bias of tech towards, put quickly, upperclass white males in their 20s or 30s. I happen to be in that category, but this makes me uncomfortable to recommend AOC as a generally suitable learning tool. It’s definitely fun to go through some of the problems, but the competition is just not for most people.

If you’re subject to obsession, AOC can take your mind off of things that might matter more than expanding a skillset, such as sleep. I found myself pondering on problems until late in the night because I wanted to stay on track with problems.

Overall, I think the design poorly takes into consideration the well-being of participants. The primary reason is the competitive format, I believe (solving problems quickly gives more points). Ignoring it is hard and feels like being left out.

## Closing thoughts

While AOC has definitely helped me get a solid foot into Rust as a language, its fundamentally exclusive design leads me to not really recommend it as a learning tool. For most people, it might result in a frustration and perhaps diminishing experience. I don’t think I’ll participate again next year. If there are any problem-oriented, but more self-paced and non-competitive tools, I think I’d rather recommend those instead.
