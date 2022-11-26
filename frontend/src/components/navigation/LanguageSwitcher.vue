/* eslint-disable */
<template lang="pug">
//- Set the width, so that the svg does not scale to its 900x600 size
v-btn.pa-0(text icon @click="switchLanguage()")
  v-icon mdi-translate
  //- alternatively use language image
  //- v-img(:src="switchLanguageSrc" width="10")
  //- Alternative select option
  //- select.text-uppercase(v-model="$i18n.locale")
  //-   option(v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang"
  //-     ) {{ lang }}
</template>

<script>
export default {
  name: "LocaleChanger",
  data: () => ({
    langs: ["de", "en"],
  }),
  methods: {
    switchLanguage() {
      if (!this.$i18n.locale || this.$i18n.locale == "en")
        this.$i18n.locale = "de";
      else if (this.$i18n.locale == "de") this.$i18n.locale = "en";
    },
  },
  computed: {
    // Which image to display
    // switchLanguageSrc() {
    //   if (!this.$i18n.locale || this.$i18n.locale == "de") {
    //     this.$i18n.locale == "de";
    //     return require("@/assets/locales/English.svg");
    //   } else return require("@/assets/locales/German.svg");
    // }
  },
};
</script>

<style scoped></style>
