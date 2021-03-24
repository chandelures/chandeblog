<template>
  <v-app-bar app color="green darken-3" dark>
    <v-container class="py-1 fill-height ">
      <v-row>
        <v-col lg="8" offset-lg="2" md="10" offset-md="1" cols="12">
          <v-avatar color="white" class="mr-8" size="35"> </v-avatar>
          <v-btn to="/" text plain> Home </v-btn>
          <v-btn to="/about" text plain> About </v-btn>
          <v-spacer> </v-spacer>
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
