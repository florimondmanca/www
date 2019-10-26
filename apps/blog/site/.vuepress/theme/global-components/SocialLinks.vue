<template>
  <ul class="u-list-reset u-flex-centerHorizontal u-flex-row">
    <li v-for="link in links" class="u-m-2">
      <a :href="link.href" :title="link.title" target="_blank" rel="noreferrer">
        <i class="fab fa-lg" :class="`fa-${link.iconName}`"></i>
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  data() {
    return {
      links: [
        [
          "https://github.com/florimondmanca",
          "GitHub (@florimondmanca)",
          "github"
        ],
        [
          "https://twitter.com/florimondmanca",
          "Twitter (@florimondmanca)",
          "twitter"
        ],
        [
          "https://www.linkedin.com/in/florimondmanca",
          "LinkedIn (florimondmanca)",
          "linkedin"
        ],
        ["https://dev.to/florimondmanca", "DEV (@florimondmanca)", "dev"]
        // TODO: RSS feed
      ].map(([href, title, iconName]) => ({
        href,
        title,
        iconName
      }))
    };
  }
};
</script>
