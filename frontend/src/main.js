import axios from "axios";
import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "./router";
import store from "./store";

import interceptorsSetup from "./helpers/interceptors";

axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;

interceptorsSetup();

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
