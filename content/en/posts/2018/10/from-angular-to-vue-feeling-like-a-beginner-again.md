---
title: "From Angular To Vue: Feeling Like A Beginner Again"
description: "I became too safe in the world of Angular, so I started learning Vue.js. Do I feel like a noob? Yes. Is it worth it? Totally."
date: "2018-10-24"
legacy_url: "/from-angular-to-vue-feeling-like-a-beginner-again"
category: retrospectives
tags:
  - webdev
  - angular
  - vue
image: "/static/img/articles/angular-vue-beginner-again.jpg"
image_thumbnail: __auto__
image_caption: "Angular, an arrow, and Vue.js."
---

I've worked on a couple of web projects in the past year or so. I now feel at ease and productive with a few select technologies. In the realm of frontend development, that means [Angular](https://angular.io). And to be honest, it feels _great_.

Yet, I find that I've begun resting on my laurels, and boredom even began to take the upper hand. As a result, I started learning [Vue](https://vuejs.org).

In this short post, I'll expose my state of mind, the difficulties I am currently encountering and what I do to cope with them in the process of **learning Vue after a year of working with Angular**.

## How did we get there?

I've worked with Angular quite extensively lately. Angular is the first modern web framework I've learnt, and I've built at least three or four different apps of various sizes. I also learnt a ton about modern concepts such as Progressive Web Apps and Server Side Rendering along the way.

But there's a catch. Every time I am given the opportunity to choose a frontend framework for a new project, I go for Angular. Why? Simply put, **because it's the only one I know and I feel comfortable with**.

Yet, immediately after taking the decision, a little voice sneaks into my head, and it whispers: "Angular, again? Meh…".

Don't get me wrong — it does feel **rewarding** to have become knowledgeable enough at a technology that I can build a whole system without barely looking at the documentation. I feel **proud**.

There's also no need _per se_ to be knowledgeable at every frontend framework out there — there are way too many of them, plus specialising also has its advantages.

But for me, there's a problem:

> Where is the challenge? Where is the difficulty? What is there left to learn?

You see, I do love learning new things. I don't particularly enjoy feeling like a beginner — that's rather uncomfortable — but I always dig the outcome: **I can do things I couldn't do before**, and it's thrilling.

That's what motivated me to try something else. Also, some circumstances have helped.

## Take your chance

I boarded on a major school project a few weeks ago. We had the possibility to choose between Angular and Vue.

I didn't know much about Vue — only a few things I've read here and there, and perhaps a toy project from a year ago. Going for Angular would have been so much easier because I've built up a lot of experience and know-how.

But guess what? We went for Vue.

Sometimes, leaving your comfort zone is as simple as asking: "why not?".

## It won't be easy

I dived in just today, and let me tell you — I'm excited, but **it feels _very_ uncomfortable** right now.

Actually, I feel **frustrated**. I have to **re-learn** everything. Why does it all look so similar, yet so different? I felt like I was a master, but I am now a total n00b. Duh.

So, in this new and unknown ecosystem, I need a **survival strategy** not to drown under the seemingly huge amount of new things to learn.

## Build on what you know

Luckily, I now have a better understanding of the world of frontend development than I had when I first tried Vue. A lot of stuff is already out of my way, and I can focus on the framework and its ecosystem. (Also, Vue has matured a lot, which is very good news.)

Quite naturally, **I am looking for what is familiar**. I have already noticed that:

- Both Angular and Vue are component-driven — great!
- Both have a [CLI](https://cli.vuejs.org) — fantastic! (but I miss `ng generate`)
- Both have a templating system based on directives — sweet!
- Both have bidirectional data binding through inputs (`@Input()` vs `@Prop()`) and outputs/events (`@Output()` vs. `$emit()`) — nice!
- The template syntax is quite similar: `*ngFor` becomes `v-for`, `[foo]="bar"` becomes `:foo="bar"`, etc — stellar!
- Both have extensive and precise [documentation](https://vuejs.org/v2/guide/), and a vibrant community — brilliant!
- I can also use [TypeScript](https://vuejs.org/v2/guide/typescript.html) with Vue — yay! 🎉
- I've been digging Angular Material, and there seems to be even more Vue component frameworks out there, like [Vuetify](https://vuetifyjs.com) — amazing!

At least, this is not a cold start. There are indeed a lot of aspects I can relate to and compare. Phew!

![Me generating a project using Vue CLI: "TypeScript! There you are!"](/static/img/angular-vue-quickstart.png)

## Identify the differences

Yet, I couldn't help but notice big differences:

- Vue components are single-file, while Angular separates HTML, CSS and TypeScript into their own files. (I'll probably get used to it.)
- **Vue focuses on the view layer**, while Angular comes batteries included: where are my beloved `Router` and `HttpClient`?!
- Vue doesn't have **modules**, and instead it has some other concepts such as mixins, filters and transitions.
- There is no concept of **services** — how am I supposed to abstract logic from components? Is that even a thing in the Vue philosophy?
- If there are no services, then what about state management? Am I forced to resort to Redux/Flux/similar even for smaller apps?
- Where are my `Observable`s? It took me so much time to get to know them. What should I use instead of [RxJS](https://angular.io/guide/rx-library)?

All of these differences gave me the general intuition that **Vue imposes much less on the developer**.

As someone with an Angular background, I find this a a bit daunting.

**Angular's conventions and ways of doing felt secure**. They also facilitated working with other devs — because we all shared the same practices. How is it going to be with Vue? Does everyone have a different workflow?

## Look for best practices and popular solutions

So what am I left with? Some stuff looks familiar, other stuff looks better (single-file components look quite slick after all), but there's also some stuff that I miss. And so I am looking for **replacements**.

Take **HTTP requests**: two popular solutions I've seen are `axios` and `vue-resource`. Looks like a good substitue for `HttpClient`.

The issue of **routing** has also been solved — there's no built-in `Router` in Vue, but [vue-router](https://router.vuejs.org) is a standard plugin that's even suggested when creating a new project via Vue CLI.

Now, what about **state management**? Angular has services and I've been lucky enough that, when data binding becomes insufficient, I could use services to store some shared state.

Vue has no such concept of services, so what's left? A popular option seems to be [vuex](https://vuex.vuejs.org), a Flux-inspired state management Vue plugin. I heard about state management before (although mostly through Redux — see [Understanding Redux](https://medium.freecodecamp.org/understanding-redux-the-worlds-easiest-guide-to-beginning-redux-c695f45546f6)), so I'm interested to dig deeper and see how that turns out. I just hope it won't be too much of a burden.

![The Vuex state management pattern. Looks sensible, but I hope it won't be too heavy. (Source: Vuex docs.)](/static/img/angular-vue-vuex.png)

Lastly — RxJS and **event streaming**. That's probably the thing I like the most in Angular. Observables make working with streams of events so pleasant and maintainable.

Well, I haven't found a substitute for that yet. My guess is — there won't be one. Actually, I suppose Vue won't get in my way and I could use RxJS, but there seems to be many built-in features already to ensure reactivity — which I also find quite exciting. We'll see!

## Enjoy the journey

I used to feel very knowledgeable about Angular, yet Vue has got me back to the position of a beginner. It's not easy, and sure as hell feels uncomfortable.

But — and this is a message to all striving beginners out there — experience also tells me that **the journey will be worth it**.

At the end of the day, you'll have learnt yet another technology, and be able to do things you couldn't do before. It may take weeks or months, but **it will happen, and you'll feel proud**. 💪

As for me, I'm not giving up on Angular just yet, but I'm excited to learn more about Vue. I will focus on building a **mental model** of how everything fits together in Vue. I look forward to the day when it all just "clicks" — because **there's nothing more exhilarating than pushing your boundaries to learn something new**. 💻

---

_Have you already been in this position? How have you coped with having to re-learn everything? I'd be happy to hear your thoughts!_
