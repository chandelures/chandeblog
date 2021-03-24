import Vue from "vue";
import "./plugins/axios";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import marked from "marked";

Vue.config.productionTip = false;
Vue.prototype.$marked = marked;

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
