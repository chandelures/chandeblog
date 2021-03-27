<template>
  <section v-if="content">
    <div class="text-h4 text-md-h3 font-weight-black mb-6" v-text="title"></div>
    <div class="text-body-2 mb-6">
      <v-avatar class="mr-3" size="35">
        <img alt="" :src="avatar" />
      </v-avatar>
      <span class="green--text text--darken-3 mr-3">chandelure</span>
      <span class="grey--text text--darken-2">{{ created | formatDate }}</span>
    </div>
    <div class="markdown-body" v-html="markdownContent" v-highlight></div>
  </section>
</template>

<script>
export default {
  name: "ArticleDetail",
  props: {
    title: String,
    content: String,
    created: String,
    avatar: String,
  },
  computed: {
    markdownContent() {
      return this.$marked(this.content);
    },
  },
};
</script>
