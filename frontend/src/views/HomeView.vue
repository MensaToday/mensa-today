<template lang="pug">
div  
  v-container.center-items
    h1 MensaToday
    v-row
      v-btn.ma-10(to="/suggestion") Daily Suggesion
      v-btn.ma-10(to="/quiz") Introduction Quiz
</template>

<script>
export default {
  name: "Home"
};
</script>