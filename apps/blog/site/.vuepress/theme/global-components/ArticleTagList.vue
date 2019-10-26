<template>
  <ul class="u-list-reset" :class="{ inline: inline }">
    <li v-for="tag in tags" class="u-mh-1">
      <router-link :to="`/tag/${tag}`">#{{ tag }}</router-link>
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    tags: {
      type: Array
    },
    inline: {
      type: Boolean,
      default: true
    }
  }
};
</script>

<style lang="stylus" scoped>
.inline {
  display: inline-flex;
  flex-wrap: wrap;
}
</style>
