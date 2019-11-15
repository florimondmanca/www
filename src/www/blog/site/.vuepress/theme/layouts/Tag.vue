<template>
  <ContentWrapper>
    <h1>Tag: #{{ tag }}</h1>
    <List :pages="pages" />
  </ContentWrapper>
</template>

<script>
import { getArticlePages } from "@theme/util";

export default {
  computed: {
    tag() {
      return this.$frontmatter.tag;
    },
    pages() {
      return getArticlePages(this.$site.pages, { tag: this.tag });
    }
  }
};
</script>
