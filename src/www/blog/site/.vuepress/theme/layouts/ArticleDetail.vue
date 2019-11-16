<template>
  <ContentWrapper>
    <header class="t-header">
      <div class="u-flex-spaceBetween u-flex-centerVertical">
        <div>
          <label class="u-color-muted" v-if="$frontmatter.date">
            {{ $frontmatter.published ? "" : "Drafted" }}
            {{ $frontmatter.date | date }}
          </label>

          <ArticleTagList
            class="t-tags"
            v-if="$frontmatter.tags"
            :tags="$frontmatter.tags"
          />
        </div>

        <a
          v-if="$isAuthenticated"
          class="p-btn p-btn--warn p-btn--icon"
          href="https://github.com/florimondmanca/blog"
          rel="no-referrer"
          target="_blank"
        >
          <i class="fa fa-edit" />
          <span>Edit on GitHub</span>
        </a>
      </div>

      <h1>
        {{ $frontmatter.title }}
      </h1>

      <p class="u-color-muted" v-if="$frontmatter.description">
        {{ $frontmatter.description }}
      </p>

      <template v-if="$frontmatter.image">
        <div class="p-image">
          <img
            :src="$withBase($frontmatter.image.path)"
            :alt="$frontmatter.image.caption"
          />
          <figcaption v-if="$frontmatter.image.caption">
            {{ $frontmatter.image.caption }}
          </figcaption>
        </div>
      </template>
    </header>

    <Content class="t-article-markdown-content" />

    <footer class="p-card">
      <h3>Stay in touch!</h3>
      <p>
        If you enjoyed this post, you can
        <a
          href="https://twitter.com/florimondmanca"
          target="_blank"
          rel="noreferrer"
          >find me on Twitter <OutboundLink
        /></a>
        for updates, announcements and news. 🐤
      </p>
      <!-- TODO -->
      <!-- <app-follow-button></app-follow-button> -->
    </footer>

    <!-- TODO -->
    <!-- <div class="nav">
      <app-post-nav
        id="previous"
        [relative]="post.previous"
        type="previous"
      ></app-post-nav>
      <app-post-nav id="next" [relative]="post.next" type="next"></app-post-nav>
    </div> -->
  </ContentWrapper>
</template>

<style lang="stylus" scoped>
@require '../styles/variables';
@require '../styles/mixins';

.t-header {
  margin-bottom: 6 * $space-unit;
  border-bottom: 1px solid $colorDivider;
}

.t-tags {
  &::before {
    content: '\2219';
  }
}
</style>

<style lang="stylus">
@require '../styles/variables';

.t-article-markdown-content {
  & h2, h3, h4, h5, h6 {
    margin-top: 8 * $space-unit;
    margin-bottom: 5 * $space-unit;
  }
}
</style>
