import axios from "axios";
import eventBus from "../BusEvent";

const setupRestClient = options => {
  axios.defaults.baseURL =
    process.env.VUE_APP_REST_HTTP ||
    (window._env && window._env.VUE_APP_REST_HTTP) ||
    "/api/v1";

  axios.defaults = {
    ...axios.defaults,
    ...options,
  };

  axios.interceptors.request.use(
    request => {
      const accessToken = localStorage.getItem("accessToken");

      if (accessToken) {
        request.headers["Authorization"] = "Bearer " + accessToken;
      }

      return request;
    },
    error => {
      return new Promise((resolve, reject) => {
        reject(error);
      });
    },
  );

  axios.interceptors.response.use(
    response => response && response.data,
    error => {
      if (error.response.status === 401) {
        eventBus.$emit("auth:relogin");
      }

      return new Promise((resolve, reject) => {
        reject(error);
      });
    },
  );

  return axios;
};

const HttpClientPlugin = {
  install: (Vue, options) => {
    Vue.prototype.$rest = setupRestClient(options);
  },
};

export { HttpClientPlugin };
export default axios;
