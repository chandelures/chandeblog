<template>
  <v-app>
    <app-bar></app-bar>

    <v-main background-color="grey lighten-3">
      <router-view> </router-view>
    </v-main>

    <app-footer></app-footer>
  </v-app>
</template>

<script>
import AppBar from "./components/AppBar.vue";
import AppFooter from "./components/AppFooter.vue";

export default {
  name: "App",

  components: {
    AppBar,
    AppFooter,
  },

  data: () => ({}),
};
</script>

<style></style>
