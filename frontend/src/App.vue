<template lang="pug">
  v-app
    v-app-bar(app='' color='primary' dark)
      .d-flex.align-center
        v-img.shrink.mr-2(alt='MensaToday Logo' contain src='@/assets/logo.png' transition='scale-transition' width='40')
        h2 MensaToday
      v-spacer
        //- something on the right side
    //- TheNavigation
    v-main
      router-view
</template>

<script>

export default {
  name: 'App',
  data: () => ({
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
