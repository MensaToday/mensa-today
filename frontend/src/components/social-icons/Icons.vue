<template lang="pug">
div.d-inline
  v-btn.mx-4.secondary--text(
    v-for="icon in iconGroup"
    :key="icon.mdi"
    icon target="_blank"
    :href="icon.link")
    v-icon(elevation="15" size="24px") {{ icon.mdi }}
</template>

<script>
export default {
  name: "SocialIcons",
  props: ["iconGroup"]
};
</script>
