---
title: Thoughts on Learning Rust with Advent of Code 2022
description: Reflections on the benefits and shortcomings of using Advent of Code to learn a new programming language.
---

Rust is just an illustration. Other people have done the same to [play with an Apple C] or learn Go or Lisp. This post is more about AOC as a learning tool, although there are specifics to Rust which I’ll cover.

Benefits

- AOC is indeed quite fun way to learn a new language, at least for the first few dozen problems.
- Small problems allow to focus on the language. Conversely, when tackling larger projects that involves libraries and frameworks, we can focus on the problems at hand or the usage of those libraries rather than bumping on the language itself. 
- The progressive difficulty makes for a progressive learning path.
- We’ve probably come across the sort of puzzles in AOC elsewhere and solved them using another language before. As  result, we can reuse our intuition from past experience and focus on the specifics of the new language, rather than getting too stuck on the problems themselves. This belongs to the general idea that reimplementing an existing solution or system (such as personal blog) is a great way to learn, I think. That’s why my next step after AOC was looking at reimplementing a blog in Rust (which led me to Axum and minijinja) and reimplementing a Solitaire game (which I did back in the day using Python and pygame, although this time I went for a terminal UI).
- The community resources around AOC are great. Reddit threads allow to lookup hints to solutions if we’re blocked while not spoiling too much — although I had a hard time not stealing solutions when I had working code under my eyes, especially as I felt pressed to finish problems as quickly as possible. Which leads  us to the shortcomings of using AOC as a language learning tool…

Shortcomings

- The difficulty ladder depends on the language. For example, Rust happens to have a notable unfriendliness to self-referencing data structures, with a trees where nodes keep references to parents and/or children. For this reason, day 5 felt like a brutal step up, as the experience transitioned from playing with arithmetics to having to implement a somewhat advanced pattern to avoid issues with the borrow checker. The Rust community is friendly and I received helpful pointers and reassurance that yes, this is a difficult thing in Rust, but that was somewhat frustrating.
- Problems end up somewhat repetitive. This is because of the “text in, number out” design of AOC. For example, 5 of the 24 problems involved parsing or modeling a 2D grid. Day 2(?) involved a 3D grid, which was refreshing.
- AOC is impossible to complete if you have any kind of life on the side, or more generally if you’re not in a situation to dedicate 2 to 4 hours a day to a programming problem in a silent place. This means AOC is structurally reinforcing the bias of tech towards, put quickly, upperclass white males in their 20s or 30s. I happen to be in that category, but this makes me uncomfortable to recommend AOC as a generally suitable learning tool. It’s definitely fun to go through some of the problems, but the competition is just not for most people.
- If you’re subject to obsession, AOC can take your mind off of things that might matter more than expanding a skillset, such as sleep. I found myself pondering on problems until late in the night because I wanted to stay on track with problems.
- Overall, I think the design poorly takes into consideration the well-being of participants. The primary reason is the competitive format, I believe (solving problems quickly gives more points). Ignoring it is hard and feels like being left out.

Conclusion

While AOC has definitely helped me get a solid foot into Rust as a language, its fundamentally exclusive design leads me to not really recommend it as a learning tool. For most people, it might result in a frustration and perhaps diminishing experience. I don’t think I’ll participate again next year. If there are any problem-oriented, but more self-paced and non-competitive tools, I think I’d rather recommend those instead.