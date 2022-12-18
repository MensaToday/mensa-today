<template lang="pug">
v-app
  v-app-bar(app color='primary' dark)
    .d-flex.align-center(@click="$router.push('/').catch(()=>{})")
      v-img.shrink.mr-2(alt='MensaToday Logo' contain src='@/assets/logo.png' transition='scale-transition' width='40')
      h2 MensaToday
    v-tabs(align-with-title v-if="$store.getters.isLoggedIn")
      v-tab.white--text(v-for="view in views" :key="view.to.name" :to="view.to") 
        v-icon.mr-3 mdi-{{ view.icon }}
        | {{ view.tag }}
      v-spacer
      .d-flex.align-center.mr-6(v-if="$store.state.card_balance")
        v-icon.mr-2 mdi-wallet
        p.my-auto.mr-9 €{{ $store.state.card_balance.replace('.',',') }}
        v-btn.px-3(outlined @click="logout()")
          v-icon mdi-logout
          | Logout
    v-spacer
    div.float-right
      v-btn(icon @click="toggleTheme") 
        v-icon mdi-brightness-6
  
  v-main.mb-12
    router-view
    template
  
  v-footer(dark padless)
    v-row 
      v-col.pb-0.pt-0
        v-card.secondary.white--text.text-center(flat tile)
          v-btn.mx-4.white--text(v-for='icon in icons' :key='icon.mdi' icon target="_blank" :href="icon.link")
            v-icon(size='24px' elevation='15')
                | {{ icon.mdi }}
          //- v-card-text.white--text.pt-0 Lorem ipsum
          v-divider
          div.white--text.body-2
            router-link(to="privacy-policy", style="text-decoration: none; color: inherit;")
              a.white--text(ref="privacy-policy")
                | Privacy Policy
          v-card-text.white--text
            | {{ new Date().getFullYear() }} &mdash; 
            strong Marten Jostmann, Leo Giesen, Erik Zimmermann, Marcel Reckmann, Polina Kireyeu
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "App",
  data: () => ({
    views: [
      {
        tag: "Your Mensa Week",
        to: { name: "HomeWeekRecommendation" },
        icon: "food",
      },
      // {
      //   tag: "Quiz (temporary)",
      //   to: { name: "QuizRegister" },
      //   icon: "information-outline",
      // },
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
      },
      {
        mdi: "mdi-github",
        link: "https://github.com/erikzimmermann/data-integration-recommender",
      },
    ],
  }),
  methods: {
    ...mapActions(["Logout"]),
    toggleTheme() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
      console.log("active theme: " + this.$vuetify.theme.dark);
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
  },
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
  background-image: linear-gradient(
    to right,
    $secondary 0%,
    $primary 51%,
    $secondary 100%
  );
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
  background-image: linear-gradient(
    to right,
    $secondaryLight 0%,
    $secondaryDark 51%,
    $secondaryLight 100%
  );
  &:hover {
    // change the direction of the change here
    background-position: right center;
  }
}
</style>
