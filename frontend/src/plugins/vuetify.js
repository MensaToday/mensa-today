/* eslint-disable */
import '@mdi/font/css/materialdesignicons.css';
import Vue from "vue";
import Vuetify from "vuetify/lib/framework";
Vue.use(Vuetify);
export default new Vuetify({
    theme: {
        options: {
          customProperties: true
        },
        // on user preference the active theme variable is updated in App within mounted()
        dark: false,
        themes: {
            // Choose colours
            // https://material.io/design/color/the-color-system.html#tools-for-picking-colors
            light: {
                // https://m2.material.io/resources/color/#!/?view.left=0&view.right=1&primary.color=EA5A0D
                primary: "#f37210",
                // primary: "#ea5a0d",
                // slightly changed orange to be less aggressive: #f37210 - but logo is not the same color 
                primaryLight: "#ff8b41",
                primaryDark: "#b02700",

                secondary: "#6c54d6",
                // alternative: light-blue darken-1: #039BE
                secondaryLight: "#a181ff",
                secondaryDark: "#3429a4", 
                
                success: "#34c759",
                warning: "#eac90d",
                error: "#ea0d2e",
            },
            dark: {
                // pink
                primary: "#9fa8da",
                primaryLight: "#d1d9ff",
                primaryDark: "#6f79a8",
                
                // light blue
                secondary: "#ffab91",
                secondaryLight: "#ffddc1",
                secondaryDark: "#c97b63",

                // as recommended by the Material Design Guidelines from Google
                background: "#121212",
                backgroundLight: "#383838",
                backgroundSuperLight: "#7f7f7f"
                // Access colors by: this.$vuetify.theme.themes.dark.primary = "#ffffff"
            }
        }
    },
    icons: { iconfont: "mdi" }
});
