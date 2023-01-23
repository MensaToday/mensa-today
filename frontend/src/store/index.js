import axios from "axios";
import Vue from "vue";
import Vuex, { mapState } from "vuex";
import createPersistedState from "vuex-persistedstate";
import router from "../router";

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
      food_allergies: [],
      user_ratings: [],
    },
    card_balance: null,
    dishplan: null,
    recommendations: null,
    dailyRecommendations: null,
  },
  computed: {
    ...mapState(["user"]),
  },
  getters: {
    isLoggedIn: (state) => state.access_token != null,
    userData: (state) => {
      return state.user;
    },
  },
  mutations: {
    setTokens(state, [access_token, refresh_token]) {
      state.access_token = access_token;
      state.refresh_token = refresh_token;
    },
    setToken(state, access_token) {
      state.access_token = access_token;
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
    UpdateRecommendations(state, [date, selected_side_dishes]) {
      console.log(state.recommendations[date]);
      state.recommendations[date] = selected_side_dishes;
      console.log(state.recommendations[date]);
    },
    setUserRatings(state, user_ratings) {
      state.user.user_ratings = user_ratings;
    },
    refreshToken() {
      // If the user has a refresh token the access token can be refreshed
      if (this.state.refresh_token != null) {
        axios
          .post("user/refresh/", {
            refresh: this.state.refresh_token,
          })
          .then((response) => {
            this.dispatch("initializeSession", [
              response.data.access,
              this.state.refresh_token,
            ]);
          })
          .catch((err) => {
            // If a 401 is returned the token cannot be refreshed and the user will get logged out
            if (err.response.status === 401) {
              this.commit("rmTokens");
              router.push("/login");
            }
          });
      }
    },
  },
  actions: {
    initializeSession({ commit, dispatch }, [access_token, refresh_token]) {
      // var user =  response.data.user
      commit("setTokens", [access_token, refresh_token]);

      if (access_token) {
        setTimeout(() => {
          dispatch("GetBalance");
        }, 1);
      } else console.log("Access token not set.");
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
      await axios.post("user/logout", {
        refresh_token: state.refresh_token,
      });
      // catch aborted navigation
      router.push("/login").catch(() => {});
      commit("rmTokens");
    },
    async GetBalance({ state, commit }) {
      // if the mensa card is not specified, you cannot make the API CALL
      if (!state.user.mensa_card_id) return;
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
    async GetUserRatings({ commit }) {
      let response = await axios.get("mensa/user_ratings");
      var user_ratings = response.data;
      // console.log(user_ratings)
      commit("setUserRatings", user_ratings);
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
        recommendations_per_day: 4,
      });

      var recommendations = response.data;
      commit("setRecommendations", recommendations);
    },
    async GetOneRecommendation({ commit }) {
      let response = await axios.get("mensa/get_week_recommendation");

      var recommendations = response.data;
      commit("setRecommendationsDaily", recommendations);
    },
    async UpdateSideDishSelection(
      { commit, dispatch },
      [date, selected_main_dish, selected_side_dishes]
    ) {
      commit("UpdateRecommendations", [date, selected_side_dishes]);
      // console.log(state.recommendations[date]);
      // extract IDs from side dishes
      let sel_side_dishes_ids = [];
      for (var side_dish_idx in selected_side_dishes) {
        if (selected_side_dishes[side_dish_idx].side_selected) {
          sel_side_dishes_ids.push(selected_side_dishes[side_dish_idx].dish.id);
        }
      }
      let main_side_dish_selection = {
        dishes: [
          {
            main: selected_main_dish.id,
            side_dishes: sel_side_dishes_ids,
          },
        ],
      };
      await axios.post("mensa/save_user_side_dishes", main_side_dish_selection);
      sel_side_dishes_ids = [];
      // update the recommendations
      dispatch("GetRecommendations");
    },
  },
  plugins: [createPersistedState()],
});
