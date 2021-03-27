<template>
  <v-responsive v-if="!isLoad" :min-height="pageHeight">
    <v-skeleton-loader class="mb-6" type="heading"> </v-skeleton-loader>
    <v-skeleton-loader class="mb-3" type="paragraph" v-for="i in 12" :key="i">
    </v-skeleton-loader>
  </v-responsive>
</template>

<script>
export default {
  name: "ArticleLoader",
  props: {
    isLoad: Boolean,
  },
  computed: {
    pageHeight() {
      return document.documentElement.clientHeight;
    },
  },
};
</script>
