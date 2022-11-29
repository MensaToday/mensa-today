import axios from 'axios';
import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "./router";
import store from "./store";

// withCredentials: instruction to Axios to send all requests with credentials such as
// authorization headers, TLS client certificates, or cookies (as in our case)
axios.defaults.baseURL = 'http://localhost:9999/api/v1/';
axios.defaults.headers.common['Access-Control-Allow-Origin'] = axios.defaults.baseURL;
axios.defaults.withCredentials = true;

// Handle expired tokens: 401 Unauthorized Error
// axios.interceptors.response.use(undefined, function (error) {
//   if (error) {
  //     const originalRequest = error.config;
  //     if (error.response.status === 401 && !originalRequest._retry) {
    
    //         originalRequest._retry = true;
    //         // TODO: implement logout function
    //         // store.dispatch('LogOut')
    //         return router.push('/')
    //     }
    //   }
    // })
    
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
