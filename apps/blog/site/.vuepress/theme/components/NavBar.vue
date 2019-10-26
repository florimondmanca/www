<template>
  <nav class="t-nav u-sticky-top u-pb-1 u-pt-2 u-ph-4">
    <ContentWrapper>
      <ul class="u-list-reset">
        <li>
          <h1 class="t-title u-mh-auto u-mb-0">
            <router-link to="/">
              <span class="t-brand-long">
                Florimond Manca
              </span>
              <span class="t-brand-short">
                FM
              </span>
            </router-link>
          </h1>
        </li>
        <li class="u-w-full">
          <input class="u-w-full" type="search" placeholder="Search" />
        </li>
      </ul>
    </ContentWrapper>
  </nav>
</template>

<style lang="stylus" scoped>
@require '../styles/variables';
@require '../styles/mixins';

.t-nav {
  background-color: $colorBackgroundCard;
  z-index: 100; // Float on top of page content.

  ul {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-gap: 6 * $space-unit;
    align-items: center;

    li {
      display: flex;
      align-items: center;
    }
  }
}

.t-title {
  font-size: $font-size-title;
  width: fit-content;
}

.t-brand-long {
  display: none;

  +forSize(tablet) {
    display: inline-block;
  }
}

.t-brand-short {
  +forSize(tablet) {
    display: none;
  }
}
</style>
