<template lang="pug">
  v-app
    v-app-bar(app color='primary' dark)
      .d-flex.align-center(to="/")
        v-img.shrink.mr-2(alt='MensaToday Logo' contain src='@/assets/logo.png' transition='scale-transition' width='40')
        h2 MensaToday
      v-tabs(align-with-title)
        v-spacer
        v-tab.white--text(v-for="view in views" :key="view.to.name" :to="view.to") 
          v-icon.mr-3 mdi-{{ view.icon }}
          | {{ view.tag }}
        v-spacer
        .d-flex.align-center.mr-6
          v-btn.px-3(outlined @click="logout()")
            v-icon.mr-3 mdi-logout
            | Logout
    v-main
      router-view
</template>

<script>

export default {
  name: 'App',
  data: () => ({
    views: [
      // {
      //   tag: "Home",
      //   to: { name: "Home" },
      //   icon: "home"
      // },
      {
        tag: "Your Mensa Week",
        to: { name: "Home" },
        icon: "food"
      },
      {
        tag: "Suggestion (temporary)",
        to: { name: "Suggestion" },
        icon: "food"
      },
      {
        tag: "Quiz (temporary)",
        to: { name: "Quiz" },
        icon: "information-outline"
      }
    ],
  }),
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
