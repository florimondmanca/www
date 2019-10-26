export function getArticlePages(pages, { tag } = {}) {
  return pages
    .filter(p => p.path.indexOf("/articles/") >= 0)
    .filter(p => p.frontmatter.published)
    .filter(p => (tag ? (p.frontmatter.tags || []).includes(tag) : true));
}
