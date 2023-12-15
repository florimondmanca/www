---
title: "Utterances: GitHub-powered Comments Section for Personal Sites"
description: "A short 'TIL' memo about using Utterances to add a comments section to your website, powered by GitHub issues."
date: "2020-07-22"
category: tutorials
tags:
  - meta
  - webdev
---

There are times in software when you're facing a problem, you find an off-the-shelf solution, and 20 lines of code later it _just works_.

Today I lived one of those moments.

## Meeting Utterances

I wanted to add a comments section to this blog for a while. I was reluctant to implement one myself the classical way, i.e. by storing commens into a database. This blog doesn't use a database yet (all pages are static Markdown content stored in a repo and rendered on-the-fly), so having to setup and maintain one just for comments felt like an overkill.

And so, as I was reading through issue [#430](https://pycoders.com/issues/430) of PyCoder's Weekly, I arrived onto [Redowan Delowar's blog](https://rednafi.github.io/digressions/python/2020/07/03/python-mixins.html).

There I found a lovely little comment section at the bottom of the page. The styling looked strangely similar to GitHub issues...

And so I learned that the comment section was powered by [Utterances](https://utteranc.es/).

![Preview of the comments section on `rednafi.github.io`.](/static/img/utterances-rednafi.png)

I had come across Utterances before but for some reason I had not realized how beautiful and elegant this piece of software is. So here I am, dedicating an entire blog entry to what I'd consider as a prime example of brilliant open source software.

## What is Utterances?

Utterances is an open source app built and maintained by [Jeremy Danyow](https://github.com/jdanyow) which he [announced](https://danyow.net/using-github-issues-for-blog-comments/) in 2018. It provides a lightweight web widget (an `<iframe>`) to add a comment section to a website. Comments are stored in issues of a GitHub repo of your choosing. In other words, each page gets its own issue with a comment feed, and so you benefit from the entire featureset of issues out-of-the-box. For example...

- You can edit, report and delete comments — great for moderation.
- When someone posts a comment, the Utterances bot litterally leaves a corresponding comment on the issue. So if you're watching the repo, you'll get email notifications when comments are posted to your site.

The other wonderful aspect about Utterances is how simple the entire setup really is...

## Setting up comments using Utterances

Okay, so let's say you want to use Utterances to have a little comments section of your own as well. How does it work?

The docs at [utteranc.es](https://utteranc.es) should get you everything you need, but here's the gist:

- Install the [utterances app](https://github.com/apps/utterances) on the repo you'd like to host comments on. (I used the repo of my blog, but I suppose it's just as possible to setup a dedicated repo.)
- Add this snippet on your website where you'd like the comments section to show up, configuring `<OWNER>` and `<NAME>`:

```html
<script
  async
  src="https://utteranc.es/client.js"
  repo="<OWNER>/<NAME>"
  issue-term="title"
  theme="github-light"
  crossorigin="anonymous"
></script>
```

That's it! The comments section will _auto-magically_ show up. Once logged into GitHub, folks will be able to post comments. They'll be reflected on GitHub, and you can manage them like you would manage issue comments. It's so simple and elegant it freaks me out.

Anyway, if you're interested the diff for my blog setup is available at [florimondmanca/www#83](https://github.com/florimondmanca/www/pull/83).

Alternatively, try it out right now by leaving a comment below!
