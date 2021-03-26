"use strict";

import marked from "marked";
import Vue from "vue";

let Marked = {};

Marked.install = function(Vue) {
  Vue.marked = marked;
  Object.defineProperties(Vue.prototype, {
    marked: {
      get() {
        return marked;
      },
    },
    $marked: {
      get() {
        return marked;
      },
    },
  });
};

Vue.use(Marked);

export default Marked;
