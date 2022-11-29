<template lang="pug">
div 
    v-row.mt-4
        v-col.col-9
            h3.d-inline Burger with Salad
        v-col.col-3
            h3.ma-0.text-right 3,80€
    v-row.my-0
        v-col.align-center.justify-center.d-flex.justify-space-between
            v-img(alt="beef" height="60" max-width="60" contain
                src="@/assets/dish_icons/food_preferences/rind.png")
            v-img(alt="beef" height="80" max-width="80" contain
                src="@/assets/dish_icons/nutri_scores/nutri-b.png")
            v-btn(@click="" rounded)
                v-icon mdi-navigation-variant-outline
                | Mensa am Ring
    //- Dish Image
    v-row.my-0
        v-col
            v-img(alt="Burger with Salad" width="375" max-width="100vw"
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
};
</script>