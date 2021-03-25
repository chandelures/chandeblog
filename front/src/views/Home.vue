<template>
  <v-container>
    <v-row>
      <v-col lg="2" cols="1"></v-col>
      <v-col lg="8" cols="10">
        <v-responsive max-width="690px" class="mx-auto mt-10 mb-10">
          <section
            v-for="(articlePre, index) in articlePreList"
            v-bind:key="articlePre.id"
          >
            <article-pre v-bind="articlePre"></article-pre>
            <v-divider
              class="my-6"
              v-if="index < articlePreList.length - 1"
            ></v-divider>
          </section>
          <v-pagination
            v-if="count > 1"
            class="mt-12"
            color="green darken-3"
            v-model="page"
            :length="Math.ceil(count / size)"
            :total-visible="7"
          ></v-pagination>
        </v-responsive>
      </v-col>
      <v-col lg="2" cols="1"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import ArticlePre from "../components/ArticlePre.vue";
import "../assets/style/markdown.scss";
import "highlight.js/styles/default.css";

export default {
  name: "Home",
  components: {
    ArticlePre,
  },
  data() {
    return {
      page: 1,
      size: 5,
      count: 0,
      articlePreList: [],
    };
  },
  watch: {
    page: function(newPage) {
      this.getArticlePreList(newPage);
      this.backTop();
    },
  },
  methods: {
    backTop() {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    },
    getArticlePreList(page) {
      this.axios({
        method: "get",
        url: "articles/",
        params: {
          page: page,
          size: this.size,
        },
      })
        .then((response) => {
          this.count = response.data.count;
          this.articlePreList = response.data.results;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.getArticlePreList(this.page);
  },
};
</script>

<style>
.v-pagination button {
  outline: none;
}
</style>
