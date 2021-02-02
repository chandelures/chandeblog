<template>
  <v-app-bar app color="green darken-3" dark>
    <v-container class="py-1 fill-height">
      <v-avatar color="white" class="mr-9" size="35"> </v-avatar>

      <v-btn to="/" text plain> Home </v-btn>
      <v-btn to="/about" text plain> About </v-btn>

      <v-spacer> </v-spacer>

      <v-responsive max-width="259px">
        <v-text-field
          hide-details
          background-color="white"
          light
          label="Search..."
          rounded
          single-line
        >
        </v-text-field>
      </v-responsive>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  name: "AppBar",
};
</script>