import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
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
    path: "/suggestion",
    name: "Suggestion",
    component: () =>
      import(/* webpackChunkName: "suggestion" */ "../views/Suggestion.vue"),
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
