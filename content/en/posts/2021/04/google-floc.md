---
title: "Loose Thoughts on Google's FLoC"
description: 'From cookie-based user data sharing to browser-computed label broadcasting: how Google plans to retain and expand its ads monopoly under the guise of promoting a more "private Web".'
date: "2021-04-17"
category: essays
tags:
  - web
image: "/static/img/articles/google-floc.jpg"
image_thumbnail: __auto__
image_caption: "A painting on a wall warning visitors about video surveillance. @tobiastu, unsplash.com."
---

This is an adapted and enhanced repost of an opinionated commentary I left on a discussion server about Google's FLoC (Federated Learning of Cohorts) initiative.

Spoiler: I don't like the "Google once again abusing its hegemonic position to dictate the future of the Web" vibe to it. I wish we banned targeted advertising and destroyed surveillance capitalism altogether instead. But this wouldn't be in Google's interest, would it? 😬

---

My awareness that there was some new hot thing called "FLoC" out there (is that pronounced "flock"?) slowly built up by bumping into recent articles such as one [instructing how a website could "opt out" of "Google's FLoC Network"](https://paramdeo.com/blog/opting-your-website-out-of-googles-floc-network). Last week, there was an HN discussion thread titled "[Brave disables Chromium FLoC features](https://news.ycombinator.com/item?id=26765084)". Anecdotically, most of the thoughts I share here actually come from answering someone who asked what FLoC was, which was itself motivated by seeing a [similar opt-out PR](https://github.com/api-platform/api-platform/pull/1879).

From afar, the mere concept of an advertising technology that requires projects and websites to opt out if they don't want to be part of it, let alone one unilateraly designed, built and implemented by a Tech giant, already seemed… _interesting_.

So I dug into it more. And in the end, things weren't exactly pretty, indeed.

## First encounter

As often, starting with the "spec" or any kind of formal description of the actual thing is a nice first step, rather than jumping to swallow someone else's analysis or opinion.

(So I encourage you to do your own research on the technology itself before reading on, as most of the following will be my own analysis and interpretation.)

After a bit of Googling (heh) I found an open GitHub repository for FLoC: [WICG/floc](https://github.com/WICG/floc).

Navigating this repo was interesting.

First, to see who were the stakeholders. The [WICG](https://www.w3.org/community/wicg/participants) (Web Platform Incubator Community Group) essentially seems to be a working group made of people from various [Big Tech](https://en.wikipedia.org/wiki/Big_Tech) companies, as well as a few researchers and other less obviously interested folks. So, okay, it's not just Google. But A/ Google executives and engineers make up a notable portion of this population, and B/ it is Google who [started deploying FLoC to Chrome users](https://plausible.io/blog/google-floc) in the past few days. So, I'll maintain the "Google's FLoC" terminology.

Then it was interesting to see how the project was being described by its creators.

## An educated newcomer's overview

From what I understand, the idea behind FLoC (which standards for "Federated Learning of Cohorts") is to replace 3rd-party cookies with in-browser classification of user interests.

Instead of the browser sharing the user's navigation history for a given domain with any third-party entity via cookies, the browser itself would analyze the user's history locally, and put the user into a "cohort", basically attaching labels that ultimately materialize as the user's "FLoC ID". This ID would be computed locally, using "machine learning" techniques (I guess some kind of clustering algorithm?), and made available via a new JavaScript API (`document.interestCohort()`) for web pages to consume.

In short, instead of telling ad marketers "here's the list of sites and web pages they visited, do whatever you want with it", browsers would tell them "here are the user's interests; treat them as such".

On the surface, this could seem like an obvious enhancement. Less data is shuffled around over the web and shared with various parties. All good, right? WRONG.

## I have questions

In my head, this raises TONS OF QUESTIONS, if only on the technical side of things. For example:

- What about the web user's acceptance (or denial) to be classified like this, or to share these "interests" (cohort memberships) with websites they visit?
- Will this be covered by GDPR and other existing regulation and legislation, or will we be entering a new privacy Far West?
- What about risks of large-scale capture of these labels, e.g. as a consequence of security breaches?
- What about other risks that come with concentrating this kind of operation in the browser?

(…And more importantly: why not throw [targeted advertising](https://en.wikipedia.org/wiki/Targeted_advertising) and [surveillance capitalism](https://en.wikipedia.org/wiki/Surveillance_capitalism) to the bin altogether? But we'll come back to this.)

## The technical fine print

Certainly, the WICG members and engineers behind this technology are competent enough to be careful about these considerations.

For example, I can read that a browser would need to put in place a mechanism so that users can send a "random" cohort rather than the "real" cohort the browser has put them in.

But these seem to be mostly stitches. For example, the "random cohorts" mechanism would be opt-in, and most likely hidden somewhere in browser settings — so what fraction of users would be disabling this? You guessed it — a tiny fraction.

There are also important questions that arise from the usage of "machine learning" techniques.

Assigning labels to users is ultimately a classification problem. As far as solutions to such problems go, AFAIK there are two main approaches:

- Unsupervised learning, e.g. using [clustering](https://en.wikipedia.org/wiki/Cluster_analysis): the algorithm determines the set of possible cohorts by itself. In this case, how do we make sure the algorithm doesn't turn into a [black box model](https://bdtechtalks.com/2020/07/27/black-box-ai-models/) nobody understands — not even their creators?
- Supervised learning (aka [statistical classification](https://en.wikipedia.org/wiki/Statistical_classification)): the list of cohorts is defined in advance. In this case, we need to see what those are, how they are defined, by whom, with what goals, what meaning is associated to them, [whether that meaning is publicly available](https://github.com/WICG/floc/issues/104), etc.

Regardless of the algorithm, the FLoC ID being some kind of opaque identifier doesn't provide transparency about the meaning of that ID — as [some have noted](https://github.com/WICG/floc/issues/101).

All in all, this seems like a continuation of the subjugation of users of the Web (and Tech in general) to an ever-expanding set of AI-powered mechanisms implemented by Tech giants. (Sorry if this sounds overly simplistic; I'm just sick of this trend, though I don't have time to develop further.)

But to me, these technical discussions are at best secondary. Focusing on them would be missing the point. There's something more fundamental and political to this story.

## The elephant in the room: Google's hegemony in action

The way I see it, FLoC is an attempt by Google to impose a new model — which they are the primary creator, although it would be defined as a standard — in order to sustain their ad-based business model. The cheesiest bit is that this comes up after they [single-handedly declared that 3rd-party cookies would go away](https://blog.chromium.org/2020/01/building-more-private-web-path-towards.html), by planning their deprecation in Chrome "within two years" starting January 2020.

In other words: kill a 25-year web technology by leveraging your browser's dominance, then come up with your own targeted ads solution.

But don't worry! As Google [revealed earlier in March](https://blog.google/products/ads-commerce/a-more-privacy-first-web/), this is to enable a "privacy-first web". Marvelous! (/sarcasm)

They even dare to present this as "no more tracking", either in the announcement or in [an answer in an issue asking about user needs](https://github.com/WICG/floc/issues/102#issuecomment-821183170) (read the entire thing; it's quite educational). Yet this is obviously not the case, as we'll see further below.

In any case, there seems to be an obvious — although legally subtle — dominant position question to this.

Let me put it with a few prospective questions. Will Google be benefiting from this "AdTech New World Order" which they are driving thanks to their hegemony? Will this be increasing barriers to entry even further? Will this be destroying competitors and other advertising actors? What will companies whose role (as shady as it was) was to process data collected through cookies and turn it into actionable insights for publishers? What will these folks become in a world where browsers themselves (which in practice means Google Chrome only — I hope Firefox and other browsers wouldn't be putting this in place) perform these computations?

In a way, I sense this technology risks **concentrating even more power and revenue into Google's hands**, increasing its domination on the Web even more.

I think that the fact that they are developing FLoC as an "open standard" is a stopgap at best. Same for doing this via this "WICG" working group with other folks from the industry. I suppose they obviously _have_ to proceed this way to protect themselves from blatant anti-trust violations. But it seems to me that they are hiding behind the "Open Web" and "Privacy" ideals, while it is clear enough that this is serving their interests in subtle and arguably shady ways.

## Dictating the Future of the Web

This story exacerbates how Google has acquired the liberty to dictate the future of the Web in ways that make any mention of [technical democracy](https://www.cairn.info/revue-journal-of-innovation-economics-2017-1-page-171.htm) or "community-driven" development of the Web feel like doublespeak.

For instance, there's this false dichotomy between on one side "old tracking" (contextual targeting, using cookies, which are so old it's about time for something new 💩), and "new tracking" (behavioral advertising, using FLoC! ✨). To any actor in the field, the only two possible reactions would be to adapt to this new state of things, or become obsolete.

But there is _at least_ a third way forward: to destroy targeted advertising and surveillance capitalism, and find new business models for the Open Web.

Obviously, this isn't in the immediate interests of Google, which still generates [about 85% of its revenue from selling ads](https://www.statista.com/statistics/266471/distribution-of-googles-revenues-by-source/) (either on their own sites, or others').

So by pushing for their own solution, Google and friends effectively dictate the future of ads on the Web, in ways that users, developers, and industry entities only have to accept and react to (like some already do by opting out of FLoC whenever they can).

## A continuation of existing trends

In a way, Google profiteering from its size and influence to govern the Web isn't new, unfortunately.

Google has [110k+ engineers](https://www.cnbc.com/2020/01/02/google-employee-growth-2001-through-2019.html). I suppose a lot of them work on internal Google products, and a substantial portion of them works on things related to the broader Web ecosystem — like developing Web standards. I assume most of these people do so in good faith.

But [like I said about QUIC and HTTP/3](https://nitter.net/florimondmanca/status/1315637400085893121), Google's influence leads to a series of events that invariably seems to repeat itself:

1. Google has a need (that derives from its massive scale, business position, or something else).
2. Google proposes a Web standard.
3. Google implements the standard in Chrome, or on another platform they control.
4. The ecosystem has to follow suit, or become obsolete.

Google certainly isn't the only Tech enterprise pushing for the Web standards they need. But it seems they've got a well-designed dynamic going for them, the cornerstone of which appears to be Google Chrome.

## Was Chrome a trojan horse?

There's a somewhat "bleeding edge" vibe to Google Chrome. After all, being Google's browser, it naturally serves as a sandbox and early-stage deployment platform for experimental Web features. When using Chrome, developers get to try the latest features, hidden under layers of feature flags, and develop websites that use the most recent features, sometimes at the expense of users\*. As Chrome has been winning the [browser wars](https://en.wikipedia.org/wiki/Browser_wars), making up over 70% of market share, it has enabled Google to look into needs they may not have been able to investigate before, resulting in them coming up with things like FLoC.

(\* From my limited experience in the web development scene, it seems certain developers tend to treat Chrome as a privileged platform to develop against. This encourages their users to prefer Chrome, either because other browsers suffer from more visual or UX bugs because of lesser QA and testing, or for more explicit reasons. For example, see [how Reddit considers Chrome](https://nitter.net/joelnet/status/1372788732953124868) as a synonym for "Web browser" on their mobile site. In B2B sectors, SaaS startups who can choose which browser their users must use semi-rationally decide to go with "Chrome-only" as the simpler and cheaper option — ignoring that this behavior reinforces Chrome's dominance.)

Some think [Chrome is the new Internet Explorer](https://erik.itland.no/chrome-is-the-new-internet-explorer-4-stages). I think that is [not true](https://news.ycombinator.com/item?id=24314251), although not for the same reasons Googlers seem to do. Perhaps it's even way worse than that.

The thing is, Chrome is _objectively_ a much more usable browser than Internet Explorer was. Users and developers like it. It also benefits from having separated out the [Chromium](https://www.chromium.org/) engine, which is now built into a variety of competitor browsers, [including Microsoft's Edge](https://www.theverge.com/2019/5/6/18527550/microsoft-chromium-edge-google-history-collaboration), Brave, or Opera, meaning Google has at least partial control over the fate of these competitors.

Ultimately, it all seems like Chrome was a trojan horse that contributed to Google reinforcing their control over the future of the Web, in ways that FLoC and the whole "Private Web" narrative reveal first-hand. Same for Google's Android on the mobile OS scene. Or Chromium OS on the lightweight desktop scene. An ever-extending monopoly, all behind "open source", "open standards". Yadda yadda yadda.

(Yes, I find Google's hegemony and ever-increasing control of all aspects of people's digital lives is _exhausting_ and, quite frankly, infuriating. 😪)

## Targeted ads must die

All in all, FLoC seems like Google single-handedly evolving the targeted ads industry by changing the approach (from a _contextual_ one to a _behavioral_ one) without changing the goal: serve Google's ad-based revenue model and hegemony.

Google is trying to push the message that behavioral advertising is more "anonymous" and "privacy-friendly", or that it would enable a "private Web".

Of course it makes sense for Google to say that.

But this is ultimately just a different approach to the same thing: profiling users to allow publishers to smash them with targeted ads, and sustain surveillance capitalism. "[Everything needs to change, so that everything can stay the same](https://en.wikipedia.org/wiki/The_Leopard#Themes_and_interpretation)".

What _are_ the paths towards a privacy-first Web — that I don't know. What I know is that that continuing to track users around the Web, even using browser-computed labels like FLoC does, definitely isn't part of it.

Until targeted ads and surveillance capitalism goes away, I recommend users [install Firefox](https://www.mozilla.org/en-US/firefox/new/), developers push back against Chrome-only web development, and people keep [de-google-ifying the Internet](https://degooglisons-internet.org/en/). It's not a lot, but that's what comes to my mind as I wrap up this piece before I once again get caught in writer's perfectionism. :-)
