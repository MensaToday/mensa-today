/* eslint-disable */
import "@mdi/font/css/materialdesignicons.css";
import Vue from "vue";
import Vuetify from "vuetify/lib/framework";
Vue.use(Vuetify);
export default new Vuetify({
  theme: {
    options: {
      customProperties: true,
    },
    dark: false,
    themes: {
      // Choose colors
      // https://material.io/design/color/the-color-system.html#tools-for-picking-colors
      light: {
        // https://m2.material.io/resources/color/#!/?view.left=0&view.right=1&primary.color=EA5A0D
        // orange
        primary: "#ff8a65",

        // dark blue
        secondary: "#233645",
        // alternative: light-blue darken-1: #039BE or purple: #6c54d6

        success: "#34c759",
        warning: "#eac90d",
        error: "#ea0d2e",
      },
      dark: {
        // pink
        primary: "#ff8a65",

        // purple
        secondary: "#233645",

        // as recommended by the Material Design Guidelines from Google
        background: "#121212",
        backgroundLight: "#383838",
        backgroundSuperLight: "#7f7f7f",
        // Access colors by: this.$vuetify.theme.themes.dark.primary = "#ffffff"
      },
    },
  },
  icons: { iconfont: "mdi" },
});
