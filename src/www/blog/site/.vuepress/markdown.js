module.exports = {
  extendMarkdown: md => {
    md.renderer.rules.image = (tokens, idx, options, env, self) => {
      // Inspired by:
      // https://github.com/markdown-it/markdown-it/blob/9ceaaa7cd98c0ddc8fd4d4d7b276616e43707226/lib/renderer.js#L89
      const token = tokens[idx];
      const src = token.attrs[token.attrIndex("src")][1];
      const alt = self.renderInlineAsText(token.children, options, env);

      return `
        <div class="p-markdown-image">
          <img src="${src}" alt="${alt}"/>
          ${alt ? `<figcaption>${alt}</figcaption>` : ""}
        </div>
      `;
    };
  }
};
