<template lang="pug">
div  
  v-container.center-items
    h1 MensaToday
    v-row
      v-btn.ma-10(to="/suggestion") Daily Suggesion
      v-btn.ma-10(to="/quiz") Introduction Quiz
    v-row 
      v-col
        h1.center-text Your Mensa Week
        v-row 
          v-col
          //- info button with ingredients
          //- browse section for all dishes on all days 
          //- -> filter out for day, location, food preference, allergies
          //- sort by rating
          //- vuetify v-data-iterator
</template>

<script>
export default {
  name: "Home"
};
</script>