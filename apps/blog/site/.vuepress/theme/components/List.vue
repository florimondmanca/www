<template>
  <div>
    <ListItem v-for="page in pages" :key="page.title" :page="page" />
    <p v-if="pages.length === 0">
      No articles yet.
    </p>
  </div>
</template>

<script>
import ListItem from "./ListItem";

export default {
  components: { ListItem },
  computed: {
    pages() {
      return this.$site.pages
        .filter(p => p.path.indexOf("/articles/") >= 0)
        .filter(p => p.frontmatter.published);
    }
  }
};
</script>
