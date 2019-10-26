---
title: "Streaming Applications with Apache Kafka: The Opening"
description: "I'm starting a series on building streaming apps with Apache Kafka — here's why!"
image:
  path: "https://images.unsplash.com/photo-1533557603879-ebdd7a92e4e8?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=6d08c991169da5df017efdbedb195909&auto=format&fit=crop&w=1050&q=80"
  caption: "Man on mountain edge. @redhatfactory, unsplash.com"
date: "2018-10-01"
published: true
tags:
  - kafka
  - announcements
---

_**Update on 15 December, 2018**: This series ended up consisting in only two (but thorough) articles. Although I promised a lot in this opening post, I didn't have the time to dive much further. I still think the contents of this series will help you navigate the wonders of Kafka, so I hope you'll enjoy your read!_

---

Great news! After some thinking, I decided to start my own **Apache Kafka series.**

Elevator pitch: [Apache Kafka](https://kafka.apache.org) is a **distributed streaming platform**. It brings together messaging capabilities, stream processing and data storage; it's fault tolerant, highly scalable and [crazy fast](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines).

I had the chance to work with Kafka in the past few months, and the experience has been, to say the least, _interesting_. It's **an extremely powerful technology**, and also rather hot/marketable at the moment. But it also has a rather steep learning curve, so I believed it would be interesting to write about it.

We won't dig down into the topic just yet. This first article will be, more than anything else, **a justification**.

TL;DR: I'm starting this series to **provide guidance and tips** for **intermediate developers** who are in the process of **learning and harnessing Apache Kafka**.

Let me explain. 🎉

## Why another introduction?

There are dozens of "Introduction to Apache Kafka" articles and series out there. You can [find](https://hackernoon.com/thorough-introduction-to-apache-kafka-6fbf2989bbc1) some [here](https://scotch.io/tutorials/an-introduction-to-apache-kafka) and [there](https://dzone.com/articles/introduction-to-apache-kafka-1) — and even [in French](https://medium.com/@AnthonyDasse/introduction-à-apache-kafka-d126f2bb852b).

So **why did I feel the need to write my own?**

It's not that similar content lacks out there or is of poor quality. In fact, you just need to make a [search on Medium](https://medium.com/search?q=kafka) to find tons of useful articles on the topic — from introductions to practical examples and more advanced concepts.

It's also not that I just wanted to make another introduction for the sake of it. I want my posts to have value, both for me and for you, the readers. The idea of a rip off just makes me cringe.

So if it's not any of that, then what is it?

## Story time

### How did I meet Kafka?

![Apache Kafka's logo.](https://www.vectorlogo.zone/logos/apache_kafka/apache_kafka-card.png)

Five months ago, while I was working as a Software Engineer Intern at [ComplyAdvantage](https://complyadvantage.com), my team was tackling a challenging problem. We needed a **fast, reliable and scalable way to implement publish/subscribe**, i.e. publish messages (or _events_) somewhere and let other systems subscribe to those messages to do their own processing.

Our initial pen-and-paper design made use of message queues in a rather cirvumvented way, and **we were not satisfied**. After discussing ideas, we decided to ditch it and go for **Apache Kafka**. And this is how a wonderful journey started…

### Finding guidance

Let's be honest — **Apache Kafka is a beast that needs to be tamed**, in every sense of the word.

Although the underlying idea — publish/subscribe — is extremely simple, there are many **concepts** in the very nature of Kafka that I was not very familiar with. I had never worked with **distributed systems** before, nor had I actually worked with **messaging systems**. But Kafka is all that — _and much more_.

So I needed **guidance**, and I found it from our Lead. Although Apache Kafka had never been used at ComplyAdvantage before, he was familiar with the concepts and the ecosystem. He was also craving for it to be pioneered because of all the advantages and how well it fitted the problems we solved day-to-day.

All of this was extremely exciting to me.

### A learning plan

Together, we established a **learning plan**.

The first step was **getting to know Kafka**: what is it? What is it _for_? What are its applications?

Then, we'd need to **learn the core concepts**: what are they, and what does each of them mean?

Only after this _initial education_ would we talk about how to use Kafka in our work.

So that was the plan, and we sticked to it. But to be honest, I went through some **hard times** in the process. Kafka concepts can be **hard to grasp** sometimes.

One thing I missed was the ability to **build something quickly**. You know, some sort of quick tutorial that inspires you and gives you confidence that the technology you're diving into is actually worth the time and effort.

## The reason why

Long story short, I want to use this series to **guide you through the process of learning and applying Kafka concepts in the real world**, beyond describing what these concepts are or represent.

Apache Kafka is a wonderful piece of technology that has a rather steep learning curve if you don't have any support or guidance.

We will take a hands-on approach and **build actual stream processing systems that solve actual problems**. FYI, most of it will be developed with **Python**.

At the end of this series, I hope you'll be **confident and knowledgeable enough** to tackle challenging problems, build real-life projects with it and **have lots of fun** along the way!

## Is this worth my time?

That's a great question! An important part of blogging is making your targeted audience clear — and write for that audience accordingly. So **who is targeted by this series?**

First, who is **not** targeted:

- **Beginners at coding/programming**. I will expect you to be at ease with at least one language (preferably Python, although you should be able to adapt if needed) and have a general knowledge of basic software engineering notions and techniques. I will make heavy use of the Terminal and use some standard tools like Docker. So if you're just getting started, you may want to look at more entry-level introductions (although starting programming with Apache Kafka may not be a great idea anyway).
- **People looking for an absolute guide**. I won't write about everything — first because because that's not possible, and second because a lot of topics are already very well covered. If you look for an definitive guide, I've read and recommend O'Reilly's [Kafka: The Definitive Guide](https://www.confluent.io/apache-kafka-stream-processing-book-bundle), but other resources exist as well.

On the other side, I think **you will be interested if**:

- You heard of (or are simply curious about) **stream processing** and you want to learn what it is and why it may be worth considering.
- You're done with making all your systems communicate through REST APIs and want to **try something else**, or need to achieve **a more reactive architecture**.
- You're getting started with Kafka and want some **guidance** in making sense of its core concepts.
- You want to see **real-world examples** of building stream processing applications.
- You are a Python developer who wants to **build modern Python streaming apps backed by Apache Kafka**.

If you fit in one of these profiles, I think you'll enjoy reading this series!

## What's next?

This was only a short opening for what will be a **series** of articles about **building streaming applications with Apache Kafka**.

Because I believe in learning by doing, the next article will have us **build our first real-world streaming application** with Apache Kafka and Python. Don't worry — we'll talk about the stream processing paradigm and Kafka core concepts later!

If you want to **start your Kafka journey today**, I'll leave you with this great article: [How to use Apache Kafka to transform a batch pipeline into a real-time one](https://medium.com/@stephane.maarek/how-to-use-apache-kafka-to-transform-a-batch-pipeline-into-a-real-time-one-831b48a6ad85). It was one of my first reads on the topic, and it is a fantastic first glimpse into how Kafka can be used to solve problems in the real world.

I'm **very excited** about this series and I hope you are too! Stay tuned. 💻
