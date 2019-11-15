const Path = require("path");
const fs = require("fs").promises;

const rstrip = (str, chars) =>
  str.endsWith(chars) ? str.slice(0, -chars.length) : str;

module.exports = (options, ctx) => {
  return {
    name: "legacy-blog-url-mapping",
    async ready() {
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
        "generated",
        "legacy-blog-url-mapping.json"
      );
      const data = JSON.stringify(urlMapping, null, 2);

      console.log("Writing legacy blog URL mapping to:", path);
      await fs.writeFile(path, data);
    }
  };
};
