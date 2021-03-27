<template>
  <v-footer
    padless
    dark
    color="green darken-3 mt-lg-10 mt-md-8 mt-sm-6 mt-4"
    min-height="70px"
  >
    <v-container>
      <v-row>
        <v-col cols="12" class="d-flex justify-center align-center">
          <div class="mr-6 d-none d-md-flex">
            <v-img
              alt="CLOG"
              src="../assets/img/logo.png"
              width="100"
              contain
            ></v-img>
          </div>
          <div class="text-caption">CopyRight © 2021 Chandelure</div>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
export default {
  name: "AppFooter",
};
</script>
