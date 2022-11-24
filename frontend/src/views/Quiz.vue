<template lang="pug">
    div
        v-container.center-items
            h1.text-center.my-8 Tell Us About Yourself - Intro-Quiz

            v-stepper(v-model='cur_step')
                v-stepper-header
                    v-stepper-step(:complete='cur_step > 1' step='1') Food Preferences
                    v-divider
                    v-stepper-step(:complete='cur_step > 2' step='2') Select Dishes
                        //- Which You Would Like to Eat
                    v-divider
                    v-stepper-step(step='3') Sign In
                v-stepper-items
                    v-stepper-content(step='1')
                        v-card.mb-4(max-width='800' flat)
                            v-row
                                v-col(cols="4" v-for="checkbox in food_preferences" :key="checkbox.food_preference")
                                    v-checkbox.mx-3(
                                        v-model="checkbox.value"
                                        :label="checkbox.food_preference")
                                v-col(cols="4")
                                    v-checkbox.mx-3(
                                        @click="isCheckAll ? uncheckAll() : checkAll()"
                                        v-model="isCheckAll"
                                        label="Select All")
                                //- p - {{food_preferences[1]["value"]}} -
                        v-btn.mb-4(color='primary' @click='cur_step = 2')
                            | Continue
                    v-stepper-content(step='2')
                        v-card.mb-4(max-width='800' flat)
                            v-row
                                v-col(
                                    v-for="dish in dishes"
                                    cols="12" sm="12" md="6"
                                    :key="dish.name")
                                    p.text-center {{dish.name}}
                                    v-img(:alt="dish.name" max-width="385"
                                        :src="require('@/assets/quiz_dishes/' + dish.img)")
                                    div.justify-center
                                        v-btn.my-2(@click="dish.would_eat = false" large width="50%" elevation="1"
                                            :color="(dish.would_eat != false) ? 'gray' : 'primary'")
                                            v-icon {{(dish.would_eat != false) ? 'mdi-thumb-down-outline' : 'mdi-thumb-down'}} 
                                        v-btn.my-2(@click="dish.would_eat = true" large width="50%" elevation="1"
                                            :color="dish.would_eat ? 'green' : 'gray'")
                                            v-icon {{(dish.would_eat && dish.would_eat != null) ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'}} 
                        v-btn(color='primary' @click='cur_step = 3')
                            | Continue
                        v-btn.ma-4(@click="cur_step-=1")
                            | Go Back
                    v-stepper-content(step='3')
                        v-card.mb-4(max-width='800' flat)
                            p Sign in to be implemented
                        v-btn(color='primary' @click='cur_step = 1')
                            | Sign In
                        v-btn.ma-4(@click="cur_step-=1")
                            | Go Back
            
            v-btn.ma-8.px-12.float-right(to="/")
                v-icon mdi-chevron-right
                | Home
</template>

<script>
export default {
    name: "Quiz",
    data: () => ({
        cur_step: 1,
        food_preferences: [
            {food_preference: "vegan",        value: false},
            {food_preference: "vegetarian",   value: false},
            {food_preference: "fish",         value: false},
            {food_preference: "pork",         value: false},
            {food_preference: "chicken",      value: false},
            {food_preference: "beef",         value: false},
            {food_preference: "alcohol",      value: false},
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
    computed: {
        isCheckAll(){
            for(let idx=0; idx<this.food_preferences.length; idx++){
                if(this.food_preferences[idx]["value"] == false) return false
            }
            return true
        }
    },
    methods: {
        checkAll(){
            for(let idx=0; idx<this.food_preferences.length; idx++){
                this.food_preferences[idx]["value"] = true
            }
        },
        uncheckAll(){
            for(let idx=0; idx<this.food_preferences.length; idx++){
                this.food_preferences[idx]["value"] = false
            }
        }
    }
};  
</script>