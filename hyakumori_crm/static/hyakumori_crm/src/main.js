import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import i18n from "./plugins/i18n";
import vuetify from "./plugins/vuetify";
import { createProvider } from "./plugins/vue-apollo";
import store from "./store";
import { intersection } from "lodash";

Vue.config.productionTip = false;

const get_scopes = () => {
  let scopes = localStorage.getItem("scopes") || "";
  scopes = scopes.split(",");
  return scopes;
};

const has_scope = scope => {
  return get_scopes().findIndex(scope) !== -1;
};

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.isPublic)) {
    next();
  } else if (localStorage.getItem("accessToken") == null) {
    next({
      path: "/auth/login",
      params: { nextUrl: to.fullPath },
    });
  } else {
    if (to.matched.some(record => record.meta.isAdmin)) {
      if (has_scope("admin")) {
        next();
      } else {
        next({ name: "error-403" });
      }
    } else {
      next();
    }

    if (
      to.matched.some(
        record =>
          record.meta.scopes &&
          record.meta.scopes.length > 0 &&
          intersection(record.meta.scopes, get_scopes()).length > 0,
      )
    ) {
      next();
    } else {
      next({ name: "error-403" });
    }
  }
});

new Vue({
  vuetify,
  store,
  i18n,
  router,
  apolloProvider: createProvider(),
  render: h => h(App),
}).$mount("#app");
