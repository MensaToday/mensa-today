import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store/index.js";
import HomeView from "../views/HomeView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
    // check if user is logged in. If yes, redirect user to user-specific page
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/quiz",
    name: "Quiz",
    component: () =>
      import(/* webpackChunkName: "quiz" */ "../views/Quiz.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/Login.vue"),
  },
  {
    path: "/suggestion",
    name: "Suggestion",
    component: () =>
      import(/* webpackChunkName: "suggestion" */ "../views/Suggestion.vue"),
    meta: { requiresAuth: true }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

// check if a user is logged in and hence, is allowed to visit a page requiring authorization 
router.beforeEach((to, from, next) => {
  // step 1: if user logged in, redirect user to user-specific page
  if(to.matched.some((record) => record.meta.isNotLoggedIn)) {
    // if logged in, the user is redirected to the home page
    if (store.getters.isLoggedIn) {
      next('/')
    }
  }

  // check if authorization is required: 
  // cf. meta tags in routes
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // if a user is logged in, he can enter
    if (store.getters.isLoggedIn) {
      // and the correct user type is given
      
      if(to.matched.some((record) => record.meta.permissionLevel == store.getters.permissionLevelString)) {
        next();
        return;
      }
    }
    // if not logged in, the user is redirected to the home page
    next("/");
  } else {
    next();
  }
});

export default router;
