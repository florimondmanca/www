<template>
  <ContentWrapper>
    <h1>Tag: #{{ tag }}</h1>
    <List :pages="pages" />
  </ContentWrapper>
</template>

<script>
import List from "../components/List.vue";
import { getArticlePages } from "../util";

export default {
  components: { List },
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
