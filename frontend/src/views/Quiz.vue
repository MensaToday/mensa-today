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
                            v-card-text
                                v-row
                                    v-col.py-0(cols="4" v-for="(value, food_preference, index) in food_preferences" :key="index")
                                        v-checkbox.mx-3(
                                            v-model="food_preferences[food_preference]"
                                            :label="food_preference")
                                    v-col.py-0(cols="4")
                                        v-checkbox.mx-3(
                                            @click="isCheckAll ? uncheckAll() : checkAll()"
                                            v-model="isCheckAll"
                                            label="Select All")
                                v-row
                                    v-col(cols="6")
                                        v-combobox(v-model='selected_allergies' :items='Object.keys(allergies)' 
                                            :search-input.sync='search' hide-selected 
                                            label='Specify Allergies' 
                                            multiple persistent-hint small-chips clearable)
                                            template(v-slot:no-data)
                                                v-list-item
                                                    v-list-item-content
                                                        v-list-item-title
                                                            | No results matching &quot;
                                                            strong {{ search }}
                                                            | &quot;. 
                                    v-col(cols="6")
                                        v-combobox(v-model='selected_additives' :items='Object.keys(additives)' 
                                            :search-input.sync='search' hide-selected 
                                            label='Specify Additives You Dislike' 
                                            multiple persistent-hint small-chips clearable)
                                            template(v-slot:no-data)
                                                v-list-item
                                                    v-list-item-content
                                                        v-list-item-title
                                                            | No results matching &quot;
                                                            strong {{ search }}
                                                            | &quot;.

                                v-card-actions
                                    v-spacer
                                    v-btn(color='primary' :disabled="no_food_preferences"
                                        @click='updateObject(allergies, selected_allergies); updateObject(additives, selected_additives); cur_step = 2')
                                        //- @click="allergies['Gluten']=true; cur_step = 2")
                                        v-icon mdi-chevron-right
                                        | Continue
                    v-stepper-content(step='2').pa-0
                        v-stepper(v-model='cur_step_dishes' tile).mt-0.pt-0
                            v-stepper-header
                                v-stepper-step(:complete='cur_step > 1' step='1')
                                v-divider
                                v-stepper-step(:complete='cur_step > 2' step='2')
                                    //- Which You Would Like to Eat
                                v-divider
                                v-stepper-step(step='3')
                            v-stepper-items
                                v-stepper-content(
                                    v-for="(dish, index) in dishes"
                                    :key="dish.name"
                                    :step='index+1')
                                    v-img.mx-auto(:alt="dish.name" max-width="395"
                                        :src="require('@/assets/quiz_dishes/' + dish.img)")
                                    div.justify-center
                                        v-btn.my-2(@click="dish.rating = 0" large width="50%" elevation="1"
                                            :color="(dish.rating != 0) ? 'gray' : 'primary'")
                                            v-icon {{(dish.rating == 0) ? 'mdi-thumb-down' : 'mdi-thumb-down-outline'}} 
                                        v-btn.my-2(@click="dish.rating = 1" large width="50%" elevation="1"
                                            :color="dish.rating ? 'green' : 'gray'")
                                            v-icon {{(dish.rating == 1) ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'}} 
                                    v-card-actions.pr-0
                                        v-btn(v-if='cur_step_dishes>1'
                                            @click="cur_step_dishes-=1") 
                                            v-icon mdi-chevron-left
                                            | Back
                                        v-spacer
                                        v-btn(color='primary' v-if='cur_step_dishes<3' :disabled="dish.rating == null"
                                            @click='cur_step_dishes++')
                                            v-icon mdi-chevron-right
                                            | Continue
                        v-card-actions
                            v-btn(@click="cur_step-=1") 
                                v-icon mdi-chevron-left
                                | Back
                            v-spacer
                            v-btn(color='primary' @click='cur_step = 3' :disabled='ratings_incomplete')
                                v-icon mdi-chevron-right
                                | Continue
                    v-stepper-content(step='3')
                        v-card.mb-4(max-width='800' flat)
                            v-card-text
                                v-form(@submit.prevent="submit")
                                    v-text-field(
                                        label="ZIV Identifier"
                                        prepend-icon="mdi-account"
                                        v-model="form.email")
                                    v-text-field(
                                        prepend-icon="mdi-lock" 
                                        v-model="form.password"
                                        label="Password" 
                                        :type="showPassword ? 'text' : 'password'"
                                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" 
                                        @click:append="showPassword = !showPassword")
                                    v-text-field(
                                        label="Mensa Card Number"
                                        prepend-icon="mdi-card-account-details"
                                        v-model="form.mensa_card_id")
                                    v-divider
                                p(v-if="showError") Identifier or Password is incorrect
                            
                            v-card-actions
                                v-btn(@click="cur_step-=1") 
                                    v-icon mdi-chevron-left
                                    | Back
                                v-spacer
                                v-btn(color="primary" @click="$router.push('/suggestion')") 
                                    v-icon mdi-chevron-right
                                    | Register                            
            
            v-btn.ma-8.px-12.float-right(to="/")
                v-icon mdi-chevron-right
                | Home
</template>

<script>
import { mapActions } from "vuex";
export default {
    name: "Quiz",
    data: () => ({
        cur_step: 1,
        cur_step_dishes: 1,
        // TODO: adjust food_preferences data structure to make food_preference the key
        food_preferences: {
            "Vegan": false,
            "Vegetarian": false,
            "Pork": false,
            "Beef": false,
            "Poultry": false,
            "Alcohol": false,
            "Fish": false,
        },
        additives: {
            "Dyed": false,
            "Preservatives": false,
            "Antioxidants": false,
            "Flavor enhancers": false,
            "Sulphurated": false,
            "Blackened": false,
            "Waxed": false,
            "Phosphate": false,
            "Sweeteners": false,
            "Phenylalanine source": false
        },
        allergies: {
            "Gluten": false,
            "Spelt": false,
            "Barles": false,
            "Oats": false,
            "Kamut": false,
            "Rye": false,
            "Wheat": false,
            "Crustaceans": false,
            "Egg": false,
            "Fish": false,
            "Peanuts": false,
            "Soy": false,
            "Milk": false,
            "Nuts": false,
            "Almonds": false,
            "Hazelnuts": false,
            "Walnuts": false,
            "Cashews": false,
            "Pecans": false,
            "Brazil nuts": false,
            "Pistachios": false,
            "Macadamias": false,
            "Celerey": false,
            "Mustard": false,
            "Sesame": false,
            "Lupines": false,
            "Molluscs": false,
            "Sulfur dioxide": false
        },
        search: null,
        selected_allergies: [],
        selected_additives: [],
        dishes: [
            {name: "Burger with Salad", img: "dish_preview.png", rating: null,
            // TODO: list of additional_ingrediants & allergies: [nuts, ...] + API Call probably needs the dish ID
            // rating: 1 if the user would eat it (thumbs up), else 0
            additional_ingrediants_allergies: [false, false, false, false, false, false, false, false, false, false, false, false]},
            {name: "Burger without Salad", img: "dish_preview.png", rating: null,
            additional_ingrediants_allergies: [false, false, false, false, false, false, false, false, false, false, false, false]},
            {name: "Burger", img: "dish_preview.png", rating: null,
            additional_ingrediants_allergies: [false, false, false, false, false, false, false, false, false, false, false, false]}
        ],
        form: {
            email: "",
            password: "",
            mensa_card_id: "",
        },
        showError: false,
        showPassword: false
    }),
    computed: {
        no_food_preferences: {
            get: function(){
                for (let [key, value] of Object.entries(this.food_preferences)) {
                    if(value == true) return false
                }
                return true
            },
            set: function(){
                return true
            }
        },
        isCheckAll: {
            get: function(){
                for (let [key, value] of Object.entries(this.food_preferences)) {
                    if(value == false) return false
                }
                return true
            },
            set: function(){
                return false
            }
        },
        ratings_incomplete: {
            get: function(){
                for(let idx = 0; idx<this.dishes.length; idx++){
                    if(this.dishes[idx]['rating'] == null) return true
                }
                return false
            },
            set: function(){
                return true
            }
        }
    },
    methods: {
        // import LogInUser action
        ...mapActions(["LogIn"]),
        checkAll(){
            Object.keys(this.food_preferences).forEach(key => {
                this.food_preferences[key] = true
            })
        },
        uncheckAll(){
            Object.keys(this.food_preferences).forEach(key => {
                this.food_preferences[key] = false
            })
        },
        updateObject(obj, values){
            for(let idx=0; idx<values.length; idx++){
                obj[values[idx]] = true
            }
        },
        async register() {
            try {
                let User = {
                    'username': this.form.email,
                    'password': this.form.password,
                    'card_id': this.form.mensa_card_id,
                    'categories': this.food_preferences,
                    'allergies': this.allergies,
                    'ratings': this.dishes
                }
                await this.Register(User);
                // Redirect to suggestion webpage
                setTimeout(() => { 
                    this.showError = false
                    this.$router.push('/suggestion')
                }, 1000);
            } catch (error) {this.showError = true}
        },
    }
};  
</script>