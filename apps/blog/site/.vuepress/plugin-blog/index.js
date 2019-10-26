const { capitalize } = require("./util");

module.exports = (options, ctx) => {
  return {
    name: "blog",

    extendPageData(pageCtx) {
      if (pageCtx.regularPath && pageCtx.regularPath.startsWith("/articles/")) {
        pageCtx.frontmatter.permalink = "/articles/:slug";
      }
    },

    async ready() {
      const tags = new Set();
      ctx.pages.forEach(page => {
        (page.frontmatter.tags || []).forEach(tag => tags.add(tag));
      });

      const additionalPages = Array.from(tags).map(tag => ({
        permalink: `/tag/${tag}`,
        frontmatter: {
          layout: "Layout",
          title: `${capitalize(tag)} - Florimond Manca`,
          tag
        }
      }));

      await Promise.all(additionalPages.map(page => ctx.addPage(page)));
    }
  };
};
