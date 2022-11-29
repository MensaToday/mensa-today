import axios from 'axios';
import Vue from "vue";
import Vuex from "vuex";


Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    loggedIn: false
  },
  getters: {},
  mutations: {
    loggedIn(state, loggedIn){
      state.loggedIn = loggedIn
  },
  },
  actions: {
    async Register({commit}, User){
      // console.log("Store User")
      // console.log(User)
      let response = await axios.post("user/register", User,
        // {
        // headers: {
        //   'Authorization': `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY5NjU3MTIxLCJpYXQiOjE2Njk2NTY4MjEsImp0aSI6IjI2MjI2YjM0MDM0MTQxYTA5YzY3NzMzNzgyMDkyZWZjIiwidXNlcl9pZCI6Mn0.LWa17AykufL2ncXXSPbddKKP8Z0Xum72tVeuIIQOvXs`,
        // }
        // }
      )
      console.log("response")
      console.log(response)
      commit("loggedIn", true)
    },
  },
  // async LogIn({getters, dispatch, commit}, user) {
  //   let response = await axios.post('token/auth', user)
  //   var token = response.data.access_token
  //   commit("setToken", token)
    
  //   const decodedToken = getters.decodedToken
  //   // get the id of currently logged in user
  //   const id = decodedToken.identity
    
  //   // get all data from currently logged in user 
  //   dispatch('getAllUserData', id)

  //   // enable the automatic refresh token cycle
  //   // the token needs to be decoded first, so we wait 2 seconds before we begin
  //   setTimeout(() => dispatch('AutoRefreshToken'), 2000)
  // },
});
