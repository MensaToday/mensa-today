<template lang="pug">
div(max-width="450") 
    v-row.mt-4
        v-col.col-9.pb-0
            h3.d-inline {{ dishPlan.dish.name }}
        v-col.col-3.pb-0
            h3.ma-0.text-right {{dishPlan.priceStudent }}€
    v-row.my-0
        v-col.align-center.justify-center.d-flex.justify-space-between.py-0
            v-img(alt="beef" height="60" max-width="60" contain
                src="@/assets/dish_icons/food_preferences/Beef.png")
            v-btn(:href="getGoogleMapsUrl(dishPlan.mensa.name)" rounded)
                v-icon mdi-navigation-variant-outline
                | {{ dishPlan.mensa.name }}
    //- Dish Image
    v-row.my-0
        v-col.pt-0.px-0
            //- div size = 450px with padding of 6; img size = 450-2*6 = 438
            v-img(alt="Burger with Salad" width="438" max-width="100vw"
                src="@/assets/quiz_dishes/dish_preview.png")
    //- Review & Comment Section
    v-row.mt-0.mb-4
        v-col.d-flex.justify-space-between.py-0
            v-rating(hover length="5" background-color="gray" 
                v-model="suggested_dish_rating")
            v-btn(@click="") 
                v-icon mdi-comment-outline
                | comment
</template>

<script>
export default {
  name: "SingleDish",
  data: () => ({
    suggested_dish_rating: null,
  }),
  props: ["dishPlan"],
  methods: {
    getGoogleMapsUrl(mensaName) {
        const url = new URL("https://www.google.com/maps/dir/?api=1")
        url.searchParams.set("destination", mensaName)
        return url.toString()
    }
  }
};
</script>
