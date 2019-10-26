<template>
  <div>
    <ListItem v-for="page in pages" :key="page.title" :page="page" />
    <p v-if="pages.length === 0">
      No articles yet.
    </p>
  </div>
</template>

<script>
export default {
  props: ["pages"]
};
</script>
