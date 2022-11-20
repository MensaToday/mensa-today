<template lang="pug">
    div  
        v-container.center-items
            h1 Tell Us About Yourself - Intro-Quiz
            h2.mt-0 1. Specify Your Food Preference
            v-row.d-flex
                v-checkbox.mx-4(
                    v-for="checkbox in food_preferences"
                    v-model="checkbox.value"
                    :key="checkbox.food_preference"
                    :label="checkbox.food_preference")
            v-row
                h2.mb-4 2. Select 3 Dishes Which You Would Like to Eat
            v-row
                v-col(
                    v-for="dish in dishes"
                    cols="12" sm="12" md="4" 
                    :key="dish.name")
                    p.text-center {{dish.name}}
                    v-img(:alt="dish.name" 
                        :src="require('@/assets/quiz_dishes/' + dish.img)")
                    div.justify-center
                        v-btn.my-2(@click="dish.would_eat = false" large width="50%" 
                            :color="(dish.would_eat != false) ? 'gray' : 'primary'")
                            v-icon {{(dish.would_eat != false) ? 'mdi-thumb-down-outline' : 'mdi-thumb-down'}} 
                        v-btn.my-2(@click="dish.would_eat = true" large width="50%" 
                            :color="dish.would_eat ? 'green' : 'gray'")
                            v-icon {{(dish.would_eat && dish.would_eat != null) ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'}} 
            v-btn.ma-2.px-12.float-right 
                v-icon mdi-chevron-right
                | continue
</template>

<script>
export default {
    name: "Quiz",
    data: () => ({
        food_preferences: [
            {food_preference: "vegan",        value: false},
            {food_preference: "vegetarian",   value: false},
            {food_preference: "fish",         value: false},
            {food_preference: "pork",         value: false},
            {food_preference: "beef",         value: false}
            ],
        dishes: [
            {name: "Burger with Salad", img: "dish_preview.png", would_eat: null,
            // TODO: list of additional_ingrediants_allergies: [nuts, ...]
            additional_ingrediants_allergies: [false, false, false, false, false, false, false, false, false, false, false, false]},
            {name: "Burger without Salad", img: "dish_preview.png", would_eat: null,
            additional_ingrediants_allergies: [false, false, false, false, false, false, false, false, false, false, false, false]},
            {name: "Burger", img: "dish_preview.png", would_eat: null,
            additional_ingrediants_allergies: [false, false, false, false, false, false, false, false, false, false, false, false]}
        ],
    }),
};
</script>