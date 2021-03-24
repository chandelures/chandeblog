<template>
  <div>
    <div class="text-h5 text-md-h4 font-weight-black mb-6">
      <router-link
        class="black--text text-decoration-none"
        :to="'/articles/' + slug"
        v-text="title"
      >
      </router-link>
    </div>
    <div class="markdown-body" v-html="markdownAbstract"></div>
    <router-link
      :to="'/articles/' + slug"
      class="text-body-2 green--text text--darken-3 text-decoration-none"
      >Read more
    </router-link>
  </div>
</template>

<script>
export default {
  name: "ArticlePre",
  props: ["title", "abstract", "slug"],
  computed: {
    markdownAbstract() {
      return this.$marked(this.abstract);
    },
  },
};
</script>
