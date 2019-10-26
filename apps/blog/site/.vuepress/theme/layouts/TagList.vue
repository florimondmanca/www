<template>
  <main class="u-ph-20">
    <h1>Hello, {{ tag }}!</h1>
  </main>
</template>

<script>
export default {
  computed: {
    tag() {
      return this.$frontmatter.tag;
    }
  }
};
</script>
