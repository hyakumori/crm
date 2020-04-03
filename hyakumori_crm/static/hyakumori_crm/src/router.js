import Vue from "vue";
import VueRouter from "vue-router";
import Forest from "./screens/Forest.vue";
import Customer from "./screens/Customer.vue";
import Archive from "./screens/Archive.vue";

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {
      path: "/forests",
      name: "forests",
      component: Forest,
    },
    {
      path: "/customers",
      name: "customers",
      component: Customer,
    },
    {
      path: "/archives",
      name: "archives",
      component: Archive,
    },
  ],
});

export default router;
