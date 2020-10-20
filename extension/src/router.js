import Vue from "vue";
import VueRouter from "vue-router";

import Data from "./views/Data";

Vue.use(VueRouter);

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "data",
      component: Data,
    },
  ],
});

export default router;
