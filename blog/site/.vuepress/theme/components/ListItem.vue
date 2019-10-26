<template>
  <article class="t-item">
    <div class="t-post-header">
      <label class="u-color-muted" v-if="page.frontmatter.date">
        {{ page.frontmatter.date | date("longDate") }}
      </label>
      <ArticleTagList
        v-if="page.frontmatter.tags && page.frontmatter.tags.length > 0"
        class="t-tag-list"
        :class="{ separated: page.frontmatter.date }"
        :tags="page.frontmatter.tags"
      />
    </div>

    <h3>
      <router-link :to="page.path">
        {{ page.title }}
      </router-link>
    </h3>

    <p>
      {{ page.frontmatter.description }}
    </p>
  </article>
</template>

<script>
import ArticleTagList from "./ArticleTagList";

export default {
  components: { ArticleTagList },
  props: {
    page: {
      type: Object
    }
  }
};
</script>

<style lang="stylus" scoped>
@require '../styles/variables';
@require '../styles/mixins';

.t-item {
  padding-bottom: 1em;

  & + .t-item {
    padding-top: 1em;
    border-top: 1px solid $colorDivider;
  }
}

.t-post-header {
  font-size: smaller;

  +forSize(tablet) {
    font-size: inherit;
  }
}

.t-tag-list {
  &.separated::before {
    content: '\2219';
  }
}
</style>
