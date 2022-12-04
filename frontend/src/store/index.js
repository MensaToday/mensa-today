import { api } from '@/api';
import axios from 'axios';
import Vue from "vue";
import Vuex from "vuex";


Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    access_token: null,
    refresh_token: null,
    user: {
      name: null,
      id: null, 
      email: null,
      mensa_card_id: null,
    },
    card_balance: 4.71,
    dishplan: null
  },
  getters: {
    isLoggedIn: (state) => true // state.user.id != null,
  },
  mutations: {
    setTokens(state, { access_token, refresh_token}){
      state.access_token = access_token
      state.refresh_token = refresh_token

      // TODO: typically we sync the whole Vuex store to localStorage
      window.localStorage.setItem('access_token', access_token);
      window.localStorage.setItem('refresh_token', refresh_token);
    },
    rmTokens(state){
      state.access_token = null
      state.refresh_token = null

      // TODO: rm tokens from localstorage
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
    async Register({commit}, user){
      const { access, refresh} = await api.register(user)
      commit("setUser", user)
      commit("setTokens", {
        access_token: access,
        refresh_token: refresh,
      })
    },
    async Login({commit, dispatch}, userCredentials) {
      const { access, refresh } = await api.login(userCredentials)
      commit("setTokens", {
        access_token: access,
        refresh_token: refresh,
      })
      setTimeout(() => { 
        dispatch("GetDishplan")
        // dispatch("GetBalance")
      }, 1);
      

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
    async Logout({commit}) {
      await api.logout()
      commit("rmTokens")
    },
    async GetBalance({commit}) {
      const { card_balance } = await api.getBalance()
      commit("setBalance", card_balance)
    },
    async GetDishplan({commit}) {
      const dishplan = await api.getDishPlan()
      commit("setDishplan", dishplan)
    }
  },
});
