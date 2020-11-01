---
published: true
title: "Cheap and easy deployment: CaptainDuckDuck (Part 1)"
description: "Deploying web apps can be a pain. I chose CaptainDuckDuck to build my personal, Heroku-style PaaS, hassle-free."
date: "2018-07-31"
legacy_url: "/cheap-and-easy-deployment-captainduckduck-1"
category: retrospectives
tags:
  - webdev
  - captainduckduck
image:
  unsplash: "photo-1517976384346-3136801d605d"
image_caption: "@spacex, unsplash.com."
---

While working on this website, I was looking for a way to relieve the pains of deployment while keeping enough **control over the infrastructure and my budget**.

In this two-part article, we will see how **CaptainDuckDuck** helped me solve this problem by building **my own personal PaaS**.

This first part is about how I chose to try out **CaptainDuckDuck as an open-source replacement for Heroku**.

## The problem

As developers, we want to spend as much time as possible doing what we love: **building great software that satisfy our users' needs.**

However, deployment is one of those things that prevents us from doing just that.

In this day and age, **deploying a web app always include some mendatory steps** such as setting up a server, configuring a reverse proxy or enabling SSL. And even when that's done, we still have to build a deployment pipeline.

All of this takes time and it has to be done for every project. And if you ask me, **it's a pain**.

At the end of June 2018, I began a project to build a personal website (_hint: this one!_).

As usual, I set up a repo and start building on my local machine. Fast-forward a week or two and I now have a version with minimal features, ready to be released into the wild.

There I was, ready to face **the pains of deployment**. I was going to have to:

- Acquire and setup a server
- Get a domain name and configure the DNS
- Install the librairies and runtimes to run my apps
- Create and configure a database
- Get SSL certificates via Let's Encrypt
- Configure Nginx
- Setup a CI/CD pipeline to deploy via `scp`, `rsync` or something similar
- Which means setting up SSH keys
- And writing scripts to update the apps after a successful deployment…

Oh, boy.

![Francisco Gonzalez, unsplash.com.](https://images.unsplash.com/photo-1520206319821-0496cfdeb31e?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=d0eb85db76e1f6019580e02beac106fe&auto=format&fit=crop&w=1050&q=80)

To make things even more interesting, I did not have one but **two distincts apps to deploy**, because I chose to use a decoupled backend/frontend stack: a frontend app built with [Angular](https://angular.io) and a REST API backend built with Python and the [Django REST Framework](https://www.django-rest-framework.org), as depicted below.

![Simplified architecture of florimondmanca.com. What hides in the cloud?](/static/img/captainduckduck-architecture.png)

I didn't want to configure all of that. So I headed right away to the one solution that I knew could make it easier: Heroku.

## Heroku is great…

[Heroku](https://www.heroku.com) is a PaaS cloud provider that offers **managed infrastructure**. You simply create an app via the dashboard, configure add-ons (databases, message brokers, email services…) and Heroku takes care of provisioning the resources and making sure they're available. Simple, easy, peanuts.

Oh and they even give you SSL by default, provide your apps with a unique domain name, have a [neat CLI](https://devcenter.heroku.com/articles/heroku-cli) and great integrations with the most common CI/CD tools (I personnally use and love [Travis CI](https://travis-ci.org)).

![Heroku's logotype.](/static/img/captainduckduck-heroku-logo.png)

I had used Heroku in other projects and I like it a lot for **prototyping**. It's great for quickly deploying apps without spending a cent.

## … But expensive in the real world

Of course, all of this has its downsides. Heroku's free servers (or _dynos_ in their jargon) sleep after 30 minutes of inactivity — but I wanted my site to be always available. Custom domains with SSL are only available if you upgrade to a paid plan, which starts at $7/mo/app. And if you want a >10k rows Postgres database, you'll have to take the $9/mo paid plan too.

As it turns out, **using Heroku for production apps quickly becomes a luxury**. Going for Heroku for my website would have cost me around **250€/year**! 🔥💸

Because this was a non-profit personal website, I figured that 70€/year, including domain name and hosting, should be largely sufficient.

At this point, it became clear that I had to find another solution.

## Can open-source save the day?

But here's the thing: there are not that many cloud providers that offer managed infrastructure. All the ones I found ([Nanobox](https://nanobox.io) — too expensive too, [AWS Elastic Beanstalk](https://aws.amazon.com/fr/elasticbeanstalk/) — too labour intensive) did not seem fit.

Then this idea struck me: there **must** exist an open source alternative to Heroku. Let's find it!

## A solution: CaptainDuckDuck 🦆

A few days later, while browsing through blog posts on my morning bus ride, I stumbled upon [this article](https://medium.freecodecamp.org/how-i-cut-my-heroku-cost-by-400-5b9d0220ce13) whose title looked strangely appealing:

> How I built a replacement for Heroku and cut my platform costs by 4X

The article was from Kasra Bigdeli. There, he explained how he found deployment to be a pain too, because there was so much he had to do, and so much of it seemed crazily repetitive. "After all, my HTTPS is no different than other hundreds of thousands of HTTPS websites on the internet." (_Yep, I 100% agree with that._) That's how Bigdeli ended up writing and open-sourcing [CaptainDuckDuck](https://captainduckduck.com).

![CaptainDuckDuck: "Build your own PaaS in a few minutes!"](/static/img/captainduckduck-logo.png)

Put simply, **CaptainDuckDuck is an open source tool for building your own Heroku-like PaaS**. Its key highlights are, for me:

- **Own your infrastructure** — CaptainDuckDuck is installed and runs directly on your server(s)
- Use the **web interface** to manage your apps
- **Provision apps and databases** in a few clicks
- **Enable SSL by the click of a button** (finally 💕)
- Pre-defined (yet customizable) **Nginx configuration** for all your apps
- An **easy-to-use CLI** to setup CaptainDuckDuck and deploy your apps

Under the hood, CaptainDuckDuck uses standard tools you'd have had to install yourself otherwise:

- **Let's Encrypt** to manage SSL certificates
- **Nginx** to serve static content and manage routing
- **Docker** to run your apps (and CaptainDuckDuck's) in their own containers

!["CaptainDuckDuck architecture at a glance." — captainduckduck.com.](/static/img/captainduckduck-glance.png)

CaptainDuckDuck provides some pre-defined templates for Docker that can detect, install and run your apps. Think of them as Heroku's build packs.

But if you're familiar with Docker (and if not, I really recommend you check it out _right now_), you can also define your own build instructions in a `Dockerfile` fashion.

This means that **CaptainDuckDuck can run any app that can run in a Docker container** — which is, well… anything really.

## Ready, set, deploy!

At this point in time, I was really excited and couldn't wait to give CaptainDuckDuck a shot.

In part 2, I will take you through the steps I took to deploy **my own personal PaaS using CaptainDuckDuck**.

Until then, if can't wait to try it out for yourself, [head to the docs](https://captainduckduck.com/docs/get-started.html)! 💻
