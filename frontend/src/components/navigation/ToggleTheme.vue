/* eslint-disable */
<template lang="pug">
v-btn(icon @click="toggleTheme") 
    v-icon mdi-brightness-6
</template>

<script>
export default {
  name: "ToggleTheme",
  methods: {
    // toggleTheme() {
    //   this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    //   // update theme
    //   // console.log("active theme: " + this.$store.getters.ActiveTheme);
    //   localStorage.setItem("isDarkTheme", this.$vuetify.theme.dark.toString());
    // }
  },
};
</script>

<style scoped></style>
