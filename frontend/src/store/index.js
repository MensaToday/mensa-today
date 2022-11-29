import axios from 'axios';
import Vue from "vue";
import Vuex from "vuex";


Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  getters: {},
  mutations: {},
  actions: {
    async Register(User){
      await axios.post("user/register/", User)
    },
  },
  modules: {},
});
