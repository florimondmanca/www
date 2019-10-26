<template>
  <div>
    <NavBar />
    <div class="t-content">
      <main class="u-mt-6">
        <Home v-if="$page.frontmatter.home" />
        <TagList v-else-if="$page.frontmatter.tag" />
        <ArticleDetail v-else-if="isArticle" />
        <Page v-else />
      </main>
      <Footer class="u-mt-3 u-mb-6" />
    </div>
  </div>
</template>

<script>
import NavBar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./layouts/Home";
import TagList from "./layouts/TagList";
import ArticleDetail from "./layouts/ArticleDetail";
import Page from "./layouts/Page";

export default {
  isRoot: true,
  components: { NavBar, Footer, Home, TagList, ArticleDetail, Page },
  computed: {
    isArticle() {
      return this.$page.path.indexOf("/articles/") >= 0;
    }
  }
};
</script>

<style lang="stylus" scoped>
@require './styles/variables';
@require './styles/mixins';

.t-content {
  padding: 0 2 * $space-unit;

  +forSize('tablet') {
    padding: 0 8 * $space-unit;
  }
}
</style>
