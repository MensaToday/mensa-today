<template lang="pug">
div
    v-card.mx-auto.my-7(outlined color="transparent")
        v-list.center-items(style="background:transparent;")
            v-list-item-content.d-inline-block
                v-btn.elevation-0.mr-3(:to='{ name: "SettingsGeneral" }') General
                v-btn.elevation-0(:to='{ name: "SettingsPrivacy" }') Privacy 
</template>

<script>
export default {
  name: "SettingsNavigation",
};
</script>
