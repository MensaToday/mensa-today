import axios from 'axios';
import Vue from "vue";
import Vuex from "vuex";


Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    access_token: null,
    refresh_token: null
  },
  getters: {
    isLoggedIn: (state) => state.access_token != null,
  },
  mutations: {
    setTokens(state, [access_token, refresh_token]){
      state.access_token = access_token
      state.refresh_token = refresh_token
    },
  },
  actions: {
    async Register({commit}, User){
      // console.log("Store User")
      // console.log(User)
      let response = await axios.post("user/register", User)
      console.log("response")
      console.log(response)
      commit("loggedIn", true)
    },
    async Login({commit}, User_credentials) {
      console.log("Store User_credentials")
      console.log(User_credentials)
      let response = await axios.post('user/login', User_credentials)
      var access_token = response.data.access
      var refresh_token = response.data.refresh
      commit("setTokens", [access_token, refresh_token])
      
      // const decodedToken = getters.decodedToken
      // // get the id of currently logged in user
      // const id = decodedToken.identity
      
      // // get all data from currently logged in user 
      // dispatch('getAllUserData', id)
  
      // // enable the automatic refresh token cycle
      // // the token needs to be decoded first, so we wait 2 seconds before we begin
      // setTimeout(() => dispatch('AutoRefreshToken'), 2000)
    },
  },
});
