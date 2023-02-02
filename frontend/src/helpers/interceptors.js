import axios from "axios";
import store from "../store";

export default function setup() {
  // Add Bearer Token to every request made
  axios.interceptors.request.use(
    function (config) {
      const token = store.state.access_token;
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    function (err) {
      return Promise.reject(err);
    }
  );
}
