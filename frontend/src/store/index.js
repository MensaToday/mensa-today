import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  getters: {},
  mutations: {},
  actions: {
    // TODO: adjust register API call. This is a placeholder
    async Register(User){
      await axios.post("register/", User)
    },
  },
  modules: {},
});
