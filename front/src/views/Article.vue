<template>
  <v-container fluid>
    <v-row>
      <v-col lg="3" md="2" cols="1"></v-col>
      <v-col lg="6" md="8" cols="10">
        <v-responsive max-width="690" class="mx-auto mt-10 mb-10">
          <article-detail v-bind="article"></article-detail>
        </v-responsive>
      </v-col>
      <v-col lg="3" md="2" cols="1"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import ArticleDetail from "../components/ArticleDetail.vue";

export default {
  name: "Article",
  data() {
    return {
      article: {},
    };
  },
  components: {
    ArticleDetail,
  },
  methods: {
    getArticle() {
      this.axios({
        methods: "get",
        url: "articles/" + this.$route.params.slug + "/",
      })
        .then((response) => {
          this.article = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.getArticle();
  },
};
</script>
