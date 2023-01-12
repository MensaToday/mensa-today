<template lang="pug">
v-app
  v-app-bar(app color='primary' dark)
    .d-flex.align-center
      v-img.shrink.mr-2(v-bind:class="cursorClass" @mouseover="isHovered = true" @mouseleave="isHovered = false" alt='MensaToday Logo' contain src='@/assets/logo_no_bg.png' transition='scale-transition' width='40' @click="$router.push('/').catch(()=>{})")
      h2 MensaToday
    v-tabs(align-with-title v-if="$store.getters.isLoggedIn")
      v-tab.white--text(v-for="view in views" :key="view.to.name" :to="view.to") 
        v-icon.mr-3 mdi-{{ view.icon }}
        | {{ view.tag }}
      v-spacer
      .d-flex.align-center.mr-5(v-if="$store.state.card_balance")
        v-icon.mr-2 mdi-wallet
        label.white--text €{{ $store.state.card_balance.replace('.',',') }}
      .d-flex.align-center.mr-3
        v-btn(icon @click="toggleTheme") 
          v-icon {{ darkMode ? 'mdi-moon-waning-crescent' : 'mdi-white-balance-sunny'}}
      .d-flex.align-center.mr-5
        v-menu(offset-y width="100px")
          template(v-slot:activator="{ on, attrs }")
            v-btn.elevation-0(color="primary" dark v-bind="attrs" v-on="on")
              v-icon mdi-dots-vertical  
          v-list(width="150px")
            v-list-item(v-for="(item, index) in optionItems" :key="index" :to="item.to") {{ item.tag }}
            v-list-item(@click="logout()") Logout
              
  v-main.mb-12
    router-view
    template

  v-footer(dark padless)
    v-row 
      v-col.pb-0.pt-0
        v-card.secondary.text-center(tile)
          v-card-title.center-items
            div.mt-3
              v-btn.mx-12.white--text(plain v-for='icon in icons' :key='icon.mdi' icon target="_blank" :href="icon.link")
                div
                  v-icon(size='24px' elevation='15')
                    | {{ icon.mdi }}
                  p.mt-2 {{ icon.text }}
          v-divider
          v-card-text.white--text.text-center
            | {{ new Date().getFullYear() }} &mdash; 
            strong Marten Jostmann, Leo Giesen, Erik Zimmermann, Marcel Reckmann, Polina Kireyeu
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "App",
  data: () => ({
    isHovered: false,
    darkMode: false,
    optionItems: [
      {
        tag: "Settings",
        to: { name: "SettingsGeneral" },
        icon: "mdi-food",
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
