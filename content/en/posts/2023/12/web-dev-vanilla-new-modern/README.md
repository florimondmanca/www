---
title: "Web Development: Vanilla Is The New Modern"
description: |
    We are entering a golden era of Web Development. Web Standards have advanced so much that most tasks for building websites can be done with vanilla technology, ensuring greater durability and broader availability for users. In this post I recap some interesting ideas and principles floating out there.
date: "2023-12-15"
category: essays
tags:
  - til
---

## Vanilla Web technology considered awesome

### HTML

Need to implement a confirmation modal? Use [`<dialog>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog), broadly available since 2022:

:::demo web-dev-vanilla-new-modern/dialog.html

### CSS

The days of inconsistent and impractical CSS are gone.

Now we have broad browser support for awesome foundational features such as Flexbox, Grid, CSS variables (aka custom properties), and CSS transitions.

Even [CSS centering is a solved problem](https://moderncss.dev/complete-guide-to-centering-in-css/#xy-grid-solution):

```css
.centered {
    display: grid;
    place-items: center;
}
```

### JavaScript

[You definitely don't need jQuery anymore](https://youmightnotneedjquery.com/).

JavaScript is now equipped DOM APIs that are complete, consistent, and well-supported.

* Need to find an element? Use `document.querySelector()`.
* Need to make an HTTP request? Use `fetch()`.
* Need to toggle a class? Use `el.classList.toggle('my-class')`.
* Need to dispatch a custom event? `Use el.dispatchEvent(new CustomEvent('my-event'))`.

## An approach to JavaScript

### Progressive enhancement is back

### HTML Web Components considered awesome

Also known as "using custom elements to enhance existing HTML".
