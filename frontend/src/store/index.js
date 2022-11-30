import axios from 'axios';
import Vue from "vue";
import Vuex from "vuex";


Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    access_token: null,
    refresh_token: null,
    user: {
      id: null, 
      email: null,
      mensa_card_id: null,
    },
    card_balance: null,
    dishplan: null
  },
  getters: {
    isLoggedIn: (state) => state.access_token != null,
  },
  mutations: {
    setTokens(state, [access_token, refresh_token]){
      state.access_token = access_token
      state.refresh_token = refresh_token
    },
    rmTokens(state){
      state.access_token = null
      state.refresh_token = null
    },
    setUser(state, user){
      state.user = user
    },
    setBalance(state, card_balance){
      state.card_balance = card_balance
    },
    setDishplan(state, dishplan) {
      state.dishplan = dishplan
    }
  },
  actions: {
    async Register({commit}, User){
      await axios.post("user/register", User)
      commit("setUser", User)
    },
    async Login({commit}, User_credentials) {
      let response = await axios.post('user/login', User_credentials)
      var access_token = response.data.access
      var refresh_token = response.data.refresh
      // var user =  response.data.user
      commit("setTokens", [access_token, refresh_token])
      // commit("setUser", user)
      
      // const decodedToken = getters.decodedToken
      // // get the id of currently logged in user
      // const id = decodedToken.identity
      
      // // get all data from currently logged in user 
      // dispatch('getAllUserData', id)
  
      // // enable the automatic refresh token cycle
      // // the token needs to be decoded first, so we wait 2 seconds before we begin
      // setTimeout(() => dispatch('AutoRefreshToken'), 2000)
    },
    // TODO: The following API-calls are in development
    async Logout(state, {commit}) {
      let response = await axios.post('user/logout', {"refresh_token": state.refresh_token})
      // var access_token = response.data.access
      // var refresh_token = response.data.refresh
      // commit("setTokens", [access_token, refresh_token])
      commit("rmTokens")
    },
    async GetBalance({commit}, card_id) {
      let response = await axios.post('user/logout', {"card_id": card_id})
      var card_balance = response.data.card_balance
      commit("setBalance", card_balance)
    },
    async GetDishplan({commit}) {
      let dishplan = await axios.post('mensa/get_dishplan')
      // var card_balance = response.data.dishplan
      commit("setDishplan", dishplan)
    }
  },
});
