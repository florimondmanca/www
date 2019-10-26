<template>
  <ContentWrapper>
    <h1>Latest posts</h1>
    <List :pages="pages" />
  </ContentWrapper>
</template>

<script>
import { getArticlePages } from "@theme/util";

export default {
  computed: {
    pages() {
      return getArticlePages(this.$site.pages);
    }
  }
};
</script>
