<template lang="pug">
    div  
        v-container.center-items
            h1.my-4.text-center Your Suggestion Today
            div
                v-divider
                //- Dish Data
                SingleDish
                v-divider 
            div 
                h1.my-4.text-center Other Options
                SingleDish(v-for="i in 2" :key="i")
            v-btn.px-12(to="/")
                v-icon mdi-chevron-left
                | go home
</template>

<script>
import SingleDish from "@/components/SingleDish.vue";
export default {
  name: "SuggestionDishes",
  components: {
    SingleDish,
  },
};
</script>
