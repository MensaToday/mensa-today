import axios from "axios";
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    access_token: null,
    refresh_token: null,
    user: {
      username: null,
      first_name: null,
      last_name: null,
      id: null,
      email: null,
      mensa_card_id: null,
      avatar: null,
      food_categories: [],
      food_allergies: []
    },
    card_balance: null,
    dishplan: null,
    recommendations: null,
    dailyRecommendations: null,
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
      window.localStorage.removeItem("access_token");
      window.localStorage.removeItem("refresh_token");
    },
    setUser(state, user) {
      state.user = user;
    },
    setBalance(state, card_balance) {
      state.card_balance = card_balance;
    },
    setUserData(state, user_data) {
      state.user.mensa_card_id = user_data.card_id;
      state.user.username = user_data.username;
      state.user.food_categories = user_data.user_category;
      state.user.food_allergies = user_data.user_allergy;
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
    initializeSession({ commit, dispatch }, [access_token, refresh_token]) {
      window.localStorage.setItem("access_token", access_token);
      window.localStorage.setItem("refresh_token", refresh_token);
      // var user =  response.data.user
      commit("setTokens", [access_token, refresh_token]);

      if (access_token) {
        axios.defaults.headers.common["Authorization"] =
          "Bearer " + access_token;

        setTimeout(() => {
          dispatch("GetBalance");
        }, 1);
      } else console.log("access token not set");
    },
    async Register({ commit, dispatch }, User) {
      let response = await axios.post("user/register", User);
      var access_token = response.data.access;
      var refresh_token = response.data.refresh;
      commit("setUser", User);
      dispatch("initializeSession", [access_token, refresh_token]);
    },
    async Login({ dispatch }, User_credentials) {
      let response = await axios.post("user/login", User_credentials);
      var access_token = response.data.access;
      var refresh_token = response.data.refresh;
      dispatch("initializeSession", [access_token, refresh_token]);
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
    async Logout({ state, commit }) {
      let response = await axios.post("user/logout", {
        refresh_token: state.refresh_token,
      });
      console.log(response);
      commit("rmTokens");
    },
    async GetBalance({ commit }) {
      let response = await axios.get("user/get_balance");
      var card_balance = response.data.toFixed(2);
      commit("setBalance", card_balance);
    },
    async GetDishplan({ commit }) {
      let response = await axios.get("mensa/get_dishplan");
      var dishplan = response.data;
      commit("setDishplan", dishplan);
    },
    async GetUserData({ commit }) {
      let response = await axios.get("user/get_user_data");
      var user_data = response.data;
      commit("setUserData", user_data);
    },
    async GetRecommendations({ commit }) {
      var today = new Date();
      var dd = String(today.getDate()).padStart(2, "0");
      var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
      var yyyy = today.getFullYear();
      today = yyyy + "." + mm + "." + dd;

      let response = await axios.post("mensa/get_recommendations", {
        day: today,
        entire_week: "True",
        recommendations_per_day: 1,
      });

      console.log(response);
      var recommendations = response.data;
      commit("setRecommendations", recommendations);
    },
    async GetOneRecommendation({ commit }) {
      let response = await axios.get("mensa/get_week_recommendation");

      var recommendations = response.data;
      commit("setRecommendationsDaily", recommendations);
    },
  },
});
