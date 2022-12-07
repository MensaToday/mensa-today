import axios from "axios";
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
    card_balance: null,
    dishplan: null,
    recommendations: null,
    dailyRecommendations: null
  },
  getters: {
    isLoggedIn: (state) => state.access_token != null,
  },
  mutations: {
    setTokens(state, [access_token, refresh_token]) {
      state.access_token = access_token;
      state.refresh_token = refresh_token;
    },
    rmTokens(state) {
      state.access_token = null;
      state.refresh_token = null;
    },
    setUser(state, user) {
      state.user = user;
    },
    setBalance(state, card_balance) {
      state.card_balance = card_balance;
    },
    setDishplan(state, dishplan) {
      state.dishplan = dishplan;
    },
    setRecommendations(state, recommendations) {
      state.recommendations = recommendations;
    },
    setRecommendationsDaily(state, recommendations) {
      state.dailyRecommendations = recommendations;
    },
  },
  actions: {
    async Register({ commit }, User) {
      await axios.post("user/register", User);
      commit("setUser", User);
    },
    async Login({ commit, dispatch }, User_credentials) {
      let response = await axios.post("user/login", User_credentials);
      var access_token = response.data.access;
      var refresh_token = response.data.refresh;
      window.localStorage.setItem("access_token", access_token);
      window.localStorage.setItem("refresh_token", refresh_token);
      // var user =  response.data.user
      commit("setTokens", [access_token, refresh_token])
      setTimeout(() => {
        dispatch("GetBalance")
      }, 1);

      if (access_token)
        axios.defaults.headers.common["Authorization"] =
          "Bearer " + access_token;

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
    async Logout({ state, commit }) {
      let response = await axios.post("user/logout", {
        refresh_token: state.refresh_token,
      });
      console.log(response);
      // var access_token = response.data.access
      // var refresh_token = response.data.refresh
      // commit("setTokens", [access_token, refresh_token])
      commit("rmTokens");
    },
    async GetBalance({commit}) {
      let response = await axios.get('user/get_balance')
      var card_balance = response.data.toFixed(2)
      commit("setBalance", card_balance)
    },
    async GetDishplan({ commit }) {
      let response = await axios.get("mensa/get_dishplan");
      var dishplan = response.data;
      commit("setDishplan", dishplan);
    },
    async GetRecommendations({commit}) {
      var today = new Date();
      var dd = String(today.getDate()).padStart(2, '0');
      var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
      var yyyy = today.getFullYear();
      today = yyyy + '.' + mm + '.' + dd;
      
      let response = await axios.post("mensa/get_recommendations", {"day": today, "entire_week": "True", "recommendations_per_day": 1})
  
      console.log(response)
      var recommendations = response.data
      commit("setRecommendations", recommendations)
    },
    async GetOneRecommendation({commit}) {
  
      let response = await axios.get("mensa/get_week_recommendation")
      
      var recommendations = response.data
      commit("setRecommendationsDaily", recommendations)
    }
  },
});
