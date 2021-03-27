<template>
  <v-container>
    <v-row>
      <v-col lg="3" md="2" sm="1" cols="0" class="d-none d-lg-flex"></v-col>
      <v-col lg="6" md="8" sm="10" cols="12" class="mx-auto">
        <v-responsive
          max-width="690px"
          class="mx-auto my-lg-10 my-md-8 my-sm-6 my-4"
        >
          <home-loader :isLoad="dataLoad"></home-loader>
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
      <v-col lg="3" md="2" sm="1" cols="0" class="d-none d-lg-flex"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import ArticlePre from "../components/ArticlePre.vue";
import "../assets/style/markdown.scss";
import "highlight.js/styles/default.css";
import HomeLoader from "../components/HomeLoader.vue";

export default {
  name: "Home",
  components: {
    ArticlePre,
    HomeLoader,
  },
  data() {
    return {
      page: 1,
      size: 5,
      count: 0,
      articlePreList: [],
      dataLoad: false,
    };
  },
  watch: {
    page: function(newPage) {
      this.dataLoad = false;
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
          this.dataLoad = true;
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
