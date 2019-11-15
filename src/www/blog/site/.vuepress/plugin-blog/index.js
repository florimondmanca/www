const Path = require("path");
const fs = require("fs").promises;
const chalk = require("chalk");
const logger = require("@vuepress/shared-utils").logger;
const { capitalize } = require("./util");

const rstrip = (str, chars) =>
  str.endsWith(chars) ? str.slice(0, -chars.length) : str;

async function generateLegacyPagesUrlMapping(ctx) {
  const urlMapping = {};
  ctx.pages
    .filter(p => p.path.indexOf("/articles/") >= 0)
    .filter(p => p.frontmatter.published)
    .filter(page => page.frontmatter.legacy_url)
    .forEach(page => {
      urlMapping[page.frontmatter.legacy_url] = rstrip(page.path, "/");
    });

  const path = Path.resolve(
    ctx.sourceDir,
    ".vuepress",
    "generated",
    "legacy-blog-url-mapping.json"
  );
  const data = JSON.stringify(urlMapping, null, 2);

  logger.info(`Write legacy blog URL mapping ${chalk.magenta(path)}`);
  await fs.writeFile(path, data);
}

async function addTagPages(ctx) {
  const tags = new Set();
  ctx.pages.forEach(page => {
    (page.frontmatter.tags || []).forEach(tag => tags.add(tag));
  });

  const additionalPages = Array.from(tags).map(tag => ({
    path: `/tag/${tag}/`,
    frontmatter: {
      layout: "Layout",
      title: `${capitalize(tag)} - Florimond Manca`,
      tag
    }
  }));

  await Promise.all(
    additionalPages.map(page => {
      logger.info(`Add tag page ${chalk.magenta(page.path)}`);
      return ctx.addPage(page);
    })
  );
}

module.exports = (options, ctx) => {
  return {
    name: "blog",

    extendPageData(page) {
      if (page.regularPath && page.regularPath.startsWith("/articles/")) {
        page.frontmatter.permalink = "/articles/:year/:month/:slug";
      }
    },

    async ready() {
      await generateLegacyPagesUrlMapping(ctx);
      await addTagPages(ctx);
    }
  };
};
