const { capitalize } = require("./util");

module.exports = (options, ctx) => {
  // TODO: compute from pages.
  const tags = ["python", "devtips"];

  const additionalPages = [];

  tags.forEach(tag =>
    additionalPages.push({
      permalink: `/t/${tag}`,
      frontmatter: {
        layout: "Layout",
        title: `${capitalize(tag)} - Florimond Manca`,
        tag
      }
    })
  );

  return {
    name: "blog",
    additionalPages
  };
};
