import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store/index.js";
import HomeView from "../views/HomeView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "HomeWeekRecommendation",
    component: HomeView,
    // check if user is logged in. If yes, redirect user to user-specific page
    meta: { requiresAuth: true },
  },
  {
    path: "/quiz",
    name: "QuizRegister",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "quiz" */ "../views/Quiz.vue"),
  },
  {
    path: "/login",
    name: "LoginUser",
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/Login.vue"),
  },
  {
    path: "/register",
    redirect: "/quiz",
  },
  {
    path: "/discover",
    name: "DiscoverDishes",
    component: () =>
      import(/* webpackChunkName: "discover" */ "../views/DiscoverDishes.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/settings/general",
    name: "SettingsGeneral",
    component: () => import(/* webpackChunkName: "discover" */ "../views/SettingsGeneral.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/settings/privacy",
    name: "SettingsPrivacy",
    component: () => import(/* webpackChunkName: "discover" */ "../views/SettingsPrivacy.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/privacy-policy",
    name: "DataPrivacy",
    component: () => import("../views/DataPrivacy.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

// check if a user is logged in and hence, is allowed to visit a page requiring authorization
router.beforeEach((to, from, next) => {
  // check if authorization is required (cf. meta tags in routes)
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // if a user is logged in, he can enter
    if (store.getters.isLoggedIn) {
      next();
      return;
    }
    // if not logged in, the user is redirected to the home page
    next("/login");
  } else {
    next();
  }
});

export default router;
