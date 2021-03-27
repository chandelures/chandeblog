<template>
  <v-app-bar color="green darken-3" dark max-height="60px">
    <v-container class="py-1 fill-height">
      <v-row>
        <v-col
          lg="8"
          offset-lg="2"
          md="10"
          offset-md="1"
          cols="12"
          class="d-flex"
        >
          <router-link class="my-auto mx-auto mr-lg-4 mr-md-2" to="/">
            <v-img alt="CBLOG" src="../assets/img/logo.png" width="100" contain>
            </v-img>
          </router-link>
          <v-btn class="d-none d-md-flex" to="/" :ripple="false" text plain>
            Home
          </v-btn>
          <v-spacer class="d-none d-md-flex"> </v-spacer>
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  name: "AppBar",
};
</script>
