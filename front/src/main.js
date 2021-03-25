import Vue from "vue";
import "./plugins/axios";
import "./plugins/highlight";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import marked from "marked";

Vue.config.productionTip = false;
Vue.prototype.$marked = marked;

Vue.filter("formatDate", (dateStr) => {
  var date = new Date(dateStr);
  var monthNames = new Array(
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Spt",
    "Oct",
    "Nov",
    "Dec"
  );
  var year = date.getFullYear();
  var month = date.getMonth();
  var day = date.getDate();
  return monthNames[month] + " " + day + ", " + year;
});

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
