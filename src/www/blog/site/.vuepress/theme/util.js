const sortDescBy = (array, getAttr) => {
  return [...array].sort((a, b) => {
    if (getAttr(a) < getAttr(b)) return 1;
    if (getAttr(a) > getAttr(b)) return -1;
    return 0;
  });
};

export function getArticlePages(pages, { tag } = {}) {
  const filteredPages = pages
    .filter(p => p.path.indexOf("/articles/") >= 0)
    .filter(p => p.frontmatter.published)
    .filter(p => (tag ? (p.frontmatter.tags || []).includes(tag) : true));
  return sortDescBy(filteredPages, p => p.frontmatter.date);
}
