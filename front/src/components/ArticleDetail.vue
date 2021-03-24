<template>
  <section>
    <div class="text-h4 text-md-h3 font-weight-black mb-6" v-text="title"></div>
    <div class="markdown-body" v-if="content" v-html="markdownContent"></div>
  </section>
</template>

<script>
export default {
  name: "ArticleDetail",
  props: ["title", "content"],
  computed: {
    markdownContent() {
      return this.$marked(this.content);
    },
  },
};
</script>
