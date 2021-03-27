<template>
  <v-responsive v-if="!isLoad" :min-height="pageHeight" @mousewheel.prevent>
  </v-responsive>
</template>

<script>
export default {
  name: "HomeLoader",
  props: {
    isLoad: Boolean,
  },
  computed: {
    pageHeight() {
      return document.documentElement.clientHeight;
    },
  },
};
</script>
