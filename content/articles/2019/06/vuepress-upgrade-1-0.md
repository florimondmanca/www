---
title: "How To Upgrade Your VuePress Site To v1.0"
description: "VuePress v1.0 is out of beta! Upgrade your documentation site by following this 10-step tutorial."
date: "2019-06-15"
legacy_url: "/vuepress-upgrade-1-0"
category: tutorials
tags:
  - webdev
  - vue
image: "/static/img/articles/vuepress-upgrade-1-0.jpg"
---

[VuePress] is a Vue-powered static site generator. It's great for writing technical documentation, and I've been using it in production for the [Bocadillo docs site](https://bocadilloproject.github.io) since December 2018.

[vuepress]: https://vuepress.vuejs.org/

I recently learnt that [VuePress v1.0 was now out of beta](https://medium.com/@_ulivz/intro-to-vuepress-1-x-7e2b7885f95f)! There are many new exciting features. The one I'm most excited about is the new **plugin architecture**. There's also a brand new [blog theme](https://github.com/ulivz/vuepress-theme-blog)!

Anyway, this means it's time to upgrade! But… how? Well, you're in luck! Today we will explore together how to upgrade your VuePress site from 0.x to 1.x. 🚀

**Note**: this post is based on my experience upgrading VuePress from 0.14 to 1.0.1 for the Bocadillo documentation. I am not a VuePress maintainer, and this is not an official guide.

## 1. Read the official announcement

Ulivz (the current maintainer of VuePress) has published a thorough blog post: [Intro to VuePress 1.x](https://medium.com/@_ulivz/intro-to-vuepress-1-x-7e2b7885f95f). It contains a lot of interesting information on what's new in 1.x, so I highly recommend you skim through it first. Hopefully it will give you even more reasons to upgrade!

## 2. Read the migration guide

The VuePress team also put up a [migration guide](https://v1.vuepress.vuejs.org/miscellaneous/migration-guide.html) on the official documentation site. I also recommend you skim through it, although we'll be covering the main changes later on.

## 3. Prepare your repo

Assuming your project is checked in Git, it's a good idea to create a new branch to explore the upgrading of VuePress. You never know whether things could go wrong, but more importantly you'll be able to review the changes by opening a PR.

So, go ahead and:

```bash
git checkout -b upgrade/vuepress-1.0
```

## 4. Upgrade VuePress

Enough already, it's time to upgrade! You can install VuePress 1.x using:

```bash
npm install vuepress@^1.0
```

It should update `package.json` with `"vuepress": "^1.0.1"` or similar, and update `package-lock.json` as well.

## 5. Use the new plugins

One of the main new features of VuePress 1.x is the [plugin architecture](https://v1.vuepress.vuejs.org/plugin/). A lot of built-in features were refactored as plugins, so we'll need to update the VuePress configuration.

### Google Analytics

Google Analytics could previously be configured via a `ga` option in the configuration object (see [0.x docs](https://vuepress.vuejs.org/config/#ga)). It is now handled by the [google-analytics](https://v1.vuepress.vuejs.org/plugin/official/plugin-google-analytics.html) plugin:

- Install the plugin:

```console
npm install @vuepress/plugin-google-analytics
```

- Edit `.vuepress/config.js` with:

```diff
module.exports = {
- ga: 'UA-12345678-9'
+ plugins: [
+   [
+     '@vuepress/google-analytics',
+     { ga: 'UA-12345678-9' }
+   ]
+ ]
}
```

(Instructions adapted from the [migration guide](https://v1.vuepress.vuejs.org/miscellaneous/migration-guide.html#ga)).

### `markdown.config`

If you were using the [`markdown.config` config option](https://vuepress.vuejs.org/config/#markdown-config) to customize the `markdown-it` instance, you should now use the `extendMarkdown` option:

- Edit `.vuepress/config.js` with:

```diff
module.exports = {
- markdown: {
-   config(md) {
-     // ...
-   }
- }
+ extendMarkdown(md) {
+   // ...
+ }
}
```

(Instructions adapted from the [migration guide](https://v1.vuepress.vuejs.org/miscellaneous/migration-guide.html#markdown-config)).

All other [Markdown options](https://v1.vuepress.vuejs.org/config/#markdown) are still valid, though.

### Service Worker

One killer feature of VuePress is the built-in Service Worker support. It allows users to access the website offline after they visited it for the first time.

Previously this was enabled via the [`serviceWorker` option](https://vuepress.vuejs.org/config/#serviceworker), but there is now a dedicated [pwa](https://v1.vuepress.vuejs.org/plugin/official/plugin-pwa.html) plugin:

- Install the plugin:

```bash
npm install @vuepress/plugin-pwa
```

- Edit `.vuepress/config.js` with:

```diff
module.exports = {
- serviceWorker: true,
+ plugins: ['@vuepress/pwa']
}
```

(Instructions adapted from the [migration guide](https://v1.vuepress.vuejs.org/plugin/official/plugin-pwa.html#migration-from-0-x)).

There are many new features that come with the `pwa` plugin, which you can learn about in the [pwa plugin docs](https://v1.vuepress.vuejs.org/plugin/official/plugin-pwa.html).

## 6. Update styles

VuePress allows you to apply [custom styles](https://v1.vuepress.vuejs.org/config/#styling) to your website, which is great to use on-brand colors and global CSS.

Previously, this could be done using `.vuepress/override.styl` (for custom colors) and `.vuepress/style.styl` (for arbitrary CSS).

VuePress 1.x now looks for these in `.vuepress/styles/palette.styl` and `.vuepress/styles/index.styl` respectively (see [migration guide](https://v1.vuepress.vuejs.org/miscellaneous/migration-guide.html#default-theme-config)). Upgrading is merely a matter of moving and renaming the existing files!

**Note**: custom themes can now also have their own copy of these, as described in [Writing a theme](https://v1.vuepress.vuejs.org/theme/writing-a-theme.html#directory-structure).

---

The points above were already covered in the official migration guide. The rest of this post focuses on extra steps I had to follow to successfully upgrade the Bocadillo documentation to use VuePress 1.x.

## 7. Update component imports

Another great feature of VuePress is that it allows you to [use Vue components in Markdown](https://v1.vuepress.vuejs.org/guide/using-vue.html), including registering your own components in `.vuepress/components`.

The default theme comes with a bunch of these components which I had been reusing in custom components of mine.

The file structure of the default theme changed, so I needed to fix the imports of these built-in components. For example:

```diff
- import NavLink from "@theme/NavLink.vue";
+ import NavLink from "@theme/components/NavLink.vue";
```

I now keep an eye on the [`theme-default`](https://github.com/vuejs/vuepress/tree/master/packages/%40vuepress/theme-default) folder to see everything that can be imported using `@theme/*`.

## 8. Fix custom layouts

The default theme in VuePress allows you to use [custom layout for specific pages](https://v1.vuepress.vuejs.org/theme/default-theme-config.html#custom-layout-for-specific-pages), i.e. replace the Vue component responsible for rendering a page with a custom one. To do this, you create a Vue component in `.vuepress/components` and specify the `layout` option in the frontmatter.

I had been using this for the layout of blog posts in the [news](https://bocadilloproject.github.io/news/) section:

```yaml
# docs/news/some-post.md
---
layout: Post
---

```

When I upgraded to 1.x, the layout was broken. I had various layout issues related to changes in the default CSS, but more specifically, the navbar wouldn't show up anymore!

![Ugh! The layout is off, and… where is my navbar?](/static/img/vuepress-layout.png)

This is because **the component given to `layout` now completely replaces the page** (including the base `Layout` component which contains the navbar, sidebar, etc.). Here, look at what [the docs](https://v1.vuepress.vuejs.org/theme/default-theme-config.html#custom-layout-for-specific-pages) say:

> If you wish to use **a completely custom component in place of the page**, you can again specify the component to use using YAML front matter:

If we want the base `<Layout>` to be included again, we need to explicitly wrap the custom layout component in it, and use one of the available [slots](https://vuejs.org/v2/guide/components-slots.html) (see [Layout.vue](https://github.com/vuejs/vuepress/blob/master/packages/%40vuepress/theme-default/layouts/Layout.vue)).

So this is how `Post.vue` now looks like:

```vue
<template>
  <Layout>
    <template slot="page-top">
      <!-- Page content… -->
    </template>
  </Layout>
</template>

<script>
import Layout from "@theme/layouts/Layout.vue";

export default {
  components: { Layout },
  // ...
};
</script>
```

Once I fixed this, the navbar was back!

## 9. Consider theme inheritance

VuePress comes with a built-in default theme, but previously customizing it was hard and you often had to **eject**. This was impractical, because you now had a lot of files which wouldn't be updated with new versions of VuePress anymore.

To fix this, VuePress 1.x comes with a brilliant new feature called [Theme inheritance](https://v1.vuepress.vuejs.org/theme/inheritance.html).

In practice, this means we can build a custom theme that extends the default theme by creating a `.vuepress/theme/index.js` file with:

```js
module.exports = {
  extends: "@vuepress/default-theme",
};
```

and then [override a particular set of components](https://v1.vuepress.vuejs.org/theme/inheritance.html#override-components) by placing them in `.vuepress/theme/components`. They will be available under the `@theme` alias just as if they came from the default theme!

**Note**: in addition to this, Vue itself also allows you to [extend components](https://alligator.io/vuejs/composing-components/#extends), which can be very useful to create a custom component based on a component included in the default theme (or any other component, really).

I didn't use this myself in the upgrade of the Bocadillo docs, so I can't go more into detail, but I thought this new feature was definitely worth sharing!

## 10. Final checks

Once you've been through the above steps, you should make sure your site runs and builds correctly before pushing it to production.

For example, you can:

- Run `vuepress dev` to start the dev server, and then go around to see if anything looks odd or broken.
- Run `vuepress build` to make sure that the build runs smoothly.
- Serve the built website to make sure there are no final cracks. I like to use Python for this: `$ python -m http.server -d path/to/.vuepress/dist`.

## Conclusion

This is it! Your VuePress website should now be upgraded to 1.x.

Hopefully this was useful to you in upgrading from 0.x, and maybe you've learnt about the new features that landed in 1.x.

If you're interested in what the upgrade looked like for me, you can take a look at the [Pull Request](https://github.com/bocadilloproject/bocadillo/pull/309/files) for the Bocadillo docs site.

Happy upgrading!
