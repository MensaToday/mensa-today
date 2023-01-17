<template lang="pug">
v-app
  NavigationBar

  v-main.mb-12
    router-view
    template

  Footer
</template>

<script>
import { mapActions } from "vuex";
import Footer from "./components/Footer.vue";
import NavigationBar from "./components/NavigationBar.vue";
export default {
  name: "App",
  components: {
    NavigationBar, Footer
  },
  created() {
    // If there is a token from a previous session, try to refresh it. 
    // In case the token expiry has passed, the logout dialog is triggered
    if (this.$store.state.access_token) {
      this.startRefreshTimer();
    }
  },
  data: () => ({
    isHovered: false,
    darkMode: false,
    optionItems: [
      {
        tag: "Settings",
        to: { name: "SettingsGeneral" },
        icon: "mdi-account-cog",
      },
    ],
    views: [
      {
        tag: "Your Mensa Week",
        to: { name: "HomeWeekRecommendation" },
        icon: "food",
      },
      {
        tag: "Discover",
        to: { name: "DiscoverDishes" },
        icon: "magnify",
      },
    ],
    icons: [
      {
        mdi: "mdi-email",
        link: "mailto:mensa.today@gmail.com",
        text: "Contact",
      },
      {
        mdi: "mdi-github",
        link: "https://github.com/erikzimmermann/data-integration-recommender",
        text: "Code",
      },
      {
        mdi: "mdi-shield-lock",
        link: "/privacy-policy",
        text: "Privacy Policy",
      },
    ],
  }),
  methods: {
    ...mapActions(["Logout"]),
    toggleTheme() {
      this.darkMode = !this.darkMode;
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    },
    async logout() {
      try {
        await this.Logout();
        // Redirect to login webpage
        setTimeout(() => {
          this.showError = false;
          this.$router.push("/login");
        }, 500);
      } catch (error) {
        console.log(error);
        this.showError = true;
      }
    },
    startRefreshTimer() {
      // time in ms
      this.$store.commit("refreshToken");
      this.timer = setInterval(() => {
        this.$store.commit("refreshToken");
      }, 3600000); // 60min*60*1000 = 3600000
    },
  },
  computed: {
    cursorClass() {
      return {
        'cursor-pointer': this.isHovered
      }
    }
  }
};
</script>

<style lang="scss">
// import of vuetify colours
$primary: var(--v-primary-base);
$primaryLight: var(--v-primaryLight-base);
$primaryDark: var(--v-primaryDark-base);
$secondary: var(--v-secondary-base);
$secondaryLight: var(--v-secondaryLight-base);
$secondaryDark: var(--v-secondaryDark-base);
$btnColor: var(--v-btnColor-base);

// $text: var(--v-text-base);
// 1. General Style
* {
  box-sizing: border-box;

  &::before,
  &::after {
    box-sizing: border-box;
  }

  // word-break: break-all !important;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  box-sizing: border-box;

  &::before,
  &::after {
    box-sizing: border-box;
  }

  // Check out cool fonts: https://visme.co/blog/modern-fonts/
  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    font-family: "Montserrat", "Prata", sans-serif !important;
    margin-top: 5rem;
    margin-bottom: 5rem;
    word-break: keep-all;
  }
}

.cursor-pointer {
  cursor: pointer;
}

.center-items {
  display: grid;
  place-items: center;
}

// 3.1 Gradient Button
.gradient-btn {
  color: $btnColor !important;
  transition: 0.5s;
  background-size: 200% auto;
  // text-shadow: 0px 0px 10px rgba(0,0,0,0.2);
  // box-shadow: 0 0 20px #eee;
  // background-image: linear-gradient(to right, $secondary 0%, $primary 51%, $secondary 100%);

  &:hover {
    // change the direction of the change here
    background-position: right center;
  }
}

.gradient-btn-secondary {
  color: $btnColor !important;
  transition: 0.5s;
  background-size: 200% auto;
  // text-shadow: 0px 0px 10px rgba(0,0,0,0.2);
  // box-shadow: 0 0 20px #eee;
  // background-image: linear-gradient(to right, $secondaryLight 0%, $secondaryDark 51%, $secondaryLight 100%);

  &:hover {
    // change the direction of the change here
    background-position: right center;
  }
}
</style>
