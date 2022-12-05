<template lang="pug">
    div
        v-container.center-items
            h1.text-center.my-8 Tell Us About Yourself - Intro-Quiz

            v-stepper(v-model='cur_step' width="500")
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
                                    v-btn(color='primary' @click="$router.push('/login')")
                                        v-icon mdi-login-variant
                                        | Login
                                    v-spacer
                                    v-btn(color='primary' :disabled="no_food_preferences"
                                        @click='updateObject(allergies, selected_allergies); updateObject(additives, selected_additives); filtered_dishes()')
                                        v-icon mdi-chevron-right
                                        | Continue
                    v-stepper-content(step='2').pa-0
                        v-stepper(v-model='cur_step_dishes' tile).mt-0.pt-0
                            v-stepper-header
                                //- p(v-if="relevantDishes") #Filtered Dishes: {{ relevantDishes.length }}
                                v-stepper-step(:complete='cur_step_dishes > 1' step='1')
                                v-divider
                                v-stepper-step(:complete='cur_step_dishes > 2' step='2')
                                v-divider
                                v-stepper-step(step='3')
                            v-stepper-items
                                v-stepper-content(
                                    v-for="(dish, index) in dishes"
                                    :key="dish.dish.name"
                                    :step='index+1')
                                    h3.my-0 {{ dish.dish.name }}
                                    v-row.my-0
                                        v-col.align-center.justify-center.d-flex.justify-space-between.py-0
                                            h3.ma-0.text-right €{{ dish.priceStudent }} / {{ dish.priceEmployee }}
                                            v-img(alt="beef" height="50" max-width="50" contain
                                                :src="require('@/assets/dish_icons/food_preferences/'+dish.dish.categories[0].category.name+'.png')")
                                            //- TODO: GMaps link here
                                            v-btn(@click="" rounded)
                                                v-icon mdi-navigation-variant-outline
                                                | {{ dish.mensa.name }} 
                                        v-img.mx-auto(:alt="dish.dish.name" 
                                            src='@/assets/quiz_dishes/dish_preview.png')
                                            v-btn(fab style="position: absolute; top: 45%; left: 4%" 
                                                v-if='cur_step_dishes>1'
                                                @click="cur_step_dishes-=1") 
                                                v-icon mdi-chevron-left
                                            v-btn(fab style="position: absolute; top: 45%; right: 4%;"
                                                v-if='cur_step_dishes<dishes.length' :disabled="dish.rating == null"
                                                @click='cur_step_dishes++')
                                                v-icon mdi-chevron-right
                                    div.justify-center
                                        v-btn.my-2(@click="dish.rating = 0; if(cur_step_dishes<dishes.length){cur_step_dishes++}" 
                                            large width="50%" elevation="1"
                                            :color="(dish.rating != 0) ? 'gray' : 'primary'")
                                            v-icon {{(dish.rating == 0) ? 'mdi-thumb-down' : 'mdi-thumb-down-outline'}} 
                                        v-btn.my-2(@click="dish.rating = 1; if(cur_step_dishes<dishes.length){cur_step_dishes++}" 
                                            large width="50%" elevation="1"
                                            :color="dish.rating ? 'green' : 'gray'")
                                            v-icon {{(dish.rating == 1) ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'}} 
                                    
                                    
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
                                p(v-if="showError") Identifier or password is incorrect
                            
                            v-card-actions
                                v-btn(@click="cur_step-=1") 
                                    v-icon mdi-chevron-left
                                    | Back
                                v-spacer
                                v-btn(color="green" @click="register()") 
                                    v-icon mdi-account-plus
                                    | Register
</template>

<script>
import dishes from "@/assets/quiz_dishes/dishes.json";
import config from "@/config.js";
import { mapActions } from "vuex";
export default {
  name: "Quiz",
  data: () => ({
    cur_step: 1,
    cur_step_dishes: 1,
    food_preferences: {
      Vegan: false,
      Vegetarian: false,
      Pork: false,
      Beef: false,
      Poultry: false,
      Alcohol: false,
      Fish: false,
    },
    additives: {
      Dyed: false,
      Preservatives: false,
      Antioxidants: false,
      "Flavor enhancers": false,
      Sulphurated: false,
      Blackened: false,
      Waxed: false,
      Phosphate: false,
      Sweeteners: false,
      "Phenylalanine source": false,
    },
    allergies: {
      Gluten: false,
      Spelt: false,
      Barles: false,
      Oats: false,
      Kamut: false,
      Rye: false,
      Wheat: false,
      Crustaceans: false,
      Egg: false,
      Fish: false,
      Peanuts: false,
      Soy: false,
      Milk: false,
      Nuts: false,
      Almonds: false,
      Hazelnuts: false,
      Walnuts: false,
      Cashews: false,
      Pecans: false,
      "Brazil nuts": false,
      Pistachios: false,
      Macadamias: false,
      Celerey: false,
      Mustard: false,
      Sesame: false,
      Lupines: false,
      Molluscs: false,
      "Sulfur dioxide": false,
    },
    search: null,
    selected_allergies: [],
    selected_additives: [],
    dishes: dishes,
    relevantDishes: null,
    form: {
      email: "",
      password: "",
      mensa_card_id: "",
    },
    overlay: true,
    showError: false,
    showPassword: false,
    publicKey: config.publicKey,
  }),
  computed: {
    no_food_preferences: {
      get: function () {
        for (let [key, value] of Object.entries(this.food_preferences)) {
          if (value == true) return false;
        }
        return true;
      },
      set: function () {
        return true;
      },
    },
    isCheckAll: {
      get: function () {
        for (let [key, value] of Object.entries(this.food_preferences)) {
          if (value == false) return false;
        }
        return true;
      },
      set: function () {
        return false;
      },
    },
    ratings_incomplete: {
      get: function () {
        for (let idx = 0; idx < this.dishes.length; idx++) {
          if (this.dishes[idx]["rating"] == null) return true;
        }
        return false;
      },
      set: function () {
        return true;
      },
    },
  },
  methods: {
    // import Register action
    ...mapActions(["Register"]),
    encrypt(m) {
      let encryptor = new JSEncrypt();
      encryptor.setPublicKey(this.publicKey);
      return encryptor.encrypt(m);
    },
    checkAll() {
      Object.keys(this.food_preferences).forEach((key) => {
        this.food_preferences[key] = true;
      });
    },
    uncheckAll() {
      Object.keys(this.food_preferences).forEach((key) => {
        this.food_preferences[key] = false;
      });
    },
    updateObject(obj, values) {
      for (let idx = 0; idx < values.length; idx++) {
        obj[values[idx]] = true;
      }
    },
    checkRelevance(user_attribute, dish_attribute, attribute_name){
        for(let idx = 0; idx < dishes.length; idx++){
            attribute = String(dish_attribute[idx])+"."+attribute_name + ".name"
            console.log(attribute)
            console.log(user_attribute[attribute])
            if(!user_attribute[attribute]) return false
        }
        return true
    },
    filtered_dishes(){
        let relevantDishes = this.dishes.filter(dish =>
            this.food_preferences[dish.dish.categories[0].category.name]  
        );
        this.dishes = relevantDishes
        this.cur_step = 2

        // this.checkRelevance(this.food_preferences, dishes.categories, "category") & 
        // this.checkRelevance(this.allergies, dishes.dish.allergies, "allergy") &
        // this.checkRelevance(this.additives, dishes.dish.additives, "additive")
    },
    async register() {
      try {
        let User = {
          username: this.form.email,
          password: this.form.password,
          card_id: this.form.mensa_card_id,
          categories: this.food_preferences,
          allergies: this.allergies,
          ratings: this.dishes,
        };
        await this.Register(User);
        // Redirect to homepage
        setTimeout(() => {
          this.showError = false;
          this.$router.push("/");
        }, 500);
      } catch (error) {
        console.log(error);
        this.showError = true;
      }
    },
  }
};
</script>
