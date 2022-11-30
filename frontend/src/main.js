import axios from 'axios';
import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "./router";
import store from "./store";

axios.defaults.baseURL = 'http://localhost:9999/api/v1/';
const access_token = store.state.access_token // localStorage.getItem('access_token');
if (access_token) {
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
}
    
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
