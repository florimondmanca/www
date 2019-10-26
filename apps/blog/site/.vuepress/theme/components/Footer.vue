<template>
  <footer>
    <ContentWrapper class="u-text-center">
      <SocialLinks />
      <p class="u-mt-2">
        © {{ year }} &middot; Made with ❤️ by Florimond Manca
      </p>
    </ContentWrapper>
  </footer>
</template>

<script>
import SocialLinks from "./SocialLinks";

export default {
  components: { SocialLinks },
  computed: {
    year() {
      return new Date().getFullYear();
    }
  }
};
</script>
