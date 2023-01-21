<template lang="pug">
v-app-bar(app color='primary' dark)
  .d-flex.align-center
    v-img.shrink.mr-2(v-bind:class="cursorClass" @mouseover="isHovered = true" @mouseleave="isHovered = false" alt='MensaToday Logo' contain src='@/assets/logo_no_bg.png' transition='scale-transition' width='40' @click="$router.push('/').catch(()=>{})")
    h2 MensaToday
  v-tabs(align-with-title v-if="$store.getters.isLoggedIn")
    v-tab.white--text(v-for="view in views" :key="view.to.name" :to="view.to") 
      v-icon mdi-{{ view.icon }}
      span.ml-3 {{ view.tag }}
    v-spacer
    .d-flex.align-center.mr-5(v-if="$store.state.card_balance")
      v-btn.elevation-0.ma-0.pa-0(href="https://topup.klarna.com/stw_munster" target="_blank" color="transparent" text)
        v-icon mdi-credit-card-plus 
      label.white--text.ml-n4 €{{ $store.state.card_balance.replace('.',',') }}
    .d-flex.align-center.mr-3
      v-btn(icon @click="toggleTheme") 
        v-icon {{ darkMode ? 'mdi-moon-waning-crescent' : 'mdi-white-balance-sunny'}}
    .d-flex.align-center.mr-5
      v-menu(offset-y width="100px")
        template(v-slot:activator="{ on, attrs }")
          v-btn.elevation-0(color="primary" dark v-bind="attrs" v-on="on")
            v-icon mdi-dots-vertical  
        v-list(width="150px")
          v-list-item(v-for="(item, index) in optionItems" :key="index" :to="item.to") 
            v-icon {{item.icon}}
            | {{ item.tag }}
          v-list-item(@click="logout()") 
            v-icon mdi-logout
            | Logout
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "NavigationBar",
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
        "cursor-pointer": this.isHovered,
      };
    },
  },
};
</script>
