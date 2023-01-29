<template lang="pug">
  div
    v-container.center-items
      h1.text-center.my-8 Tell Us About Yourself - Intro-Quiz
      v-stepper(v-model='cur_step' width="500")
        v-stepper-header
          v-stepper-step(:complete='cur_step > 1' step='1') Food Preferences
          v-divider
          v-stepper-step(:complete='cur_step > 2' step='2') Select Dishes
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
                      :search-input.sync='search' hide-selected label='Specify Allergies' 
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
                    @click='updateObject(allergies, selected_allergies); updateObject(additives, selected_additives); updateSelectedCategories(); cur_step = 2; cur_step_dishes = 1')
                    v-icon mdi-chevron-right
                    | Continue
          v-stepper-content(step='2').pa-0
            v-stepper(v-model='cur_step_dishes' tile).mt-0.pt-0
              v-stepper-header
                v-stepper-step(:complete='cur_step_dishes > 1' step='1')
                v-divider
                v-stepper-step(:complete='cur_step_dishes > 2' step='2')
                v-divider
                v-stepper-step(step='3')
              v-stepper-items
                v-stepper-content(
                  v-for="(dish, index) in dishes"
                  :key="index"
                  :step='index+1')
                  h3.my-0 {{ dish.name }}
                  v-row.my-0
                    v-col.align-center.justify-center.d-flex.justify-space-between.py-0
                      //h3.ma-0.text-right €{{ dish.priceStudent }} / {{ dish.priceEmployee }}
                      v-img(:alt="dish.categories[0].name" height="50" width="50" contain
                        :src="require('@/assets/dish_icons/food_preferences/'+dish.categories[0].name+'.png')")
                    v-img(:alt="dish.name" 
                      :src="dish.url", height='250')
                      v-btn(fab style="position: absolute; top: 45%; left: 4%" 
                        v-if='cur_step_dishes>1'
                        @click="cur_step_dishes-=1") 
                        v-icon mdi-chevron-left
                      v-btn(fab style="position: absolute; top: 45%; right: 4%;"
                        v-if='cur_step_dishes<3' 
                        :disabled="dish_ratings[index].rating == null"
                        @click='cur_step_dishes+=1')
                        v-icon mdi-chevron-right
                  div.justify-center
                    v-btn.my-2(@click="addRating(cur_step_dishes-1, dish.id, 0)" 
                      large width="50%" elevation="1"
                      :color="dish_ratings[index].rating != 0 ? 'gray' : 'primary'"
                      )
                      v-icon {{(dish_ratings[index].rating == 0) ? 'mdi-thumb-down' : 'mdi-thumb-down-outline'}} 
                    v-btn.my-2(@click="addRating(cur_step_dishes-1, dish.id, 1)" 
                      large width="50%" elevation="1"
                      :color="dish_ratings[index].rating ? 'green' : 'gray'"
                      )
                      v-icon {{(dish_ratings[index].rating == 1) ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'}} 

            v-card-actions
              v-btn(@click="initialize_dish_ratings(); cur_step-=1") 
                v-icon mdi-chevron-left
                | Back
              v-spacer
              v-btn(color='primary' @click='cur_step = 3' :disabled='dish_ratings[2].rating == null')
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
                    type="number"
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
import axios from "axios";
import JSEncrypt from "jsencrypt";
import Vue from "vue";
import { mapActions } from "vuex";
export default {
  name: "QuizRegister",
  data: () => ({
    cur_step: 1,
    cur_step_dishes: 0,
    food_preferences: {
      Vegan: true,
      Vegetarian: true,
      Pork: true,
      Beef: true,
      Poultry: true,
      Alcohol: true,
      Fish: true,
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
    selected_categories: [],
    selected_allergies: [],
    selected_additives: [],
    dishes: dishes,
    dish_ratings: [],
    form: {
      email: "",
      password: "",
      mensa_card_id: null,
    },
    showError: false,
    showPassword: false,
    publicKey: config.publicKey,
  }),
  computed: {
    no_food_preferences: {
      get: function () {
        for (let [, value] of Object.entries(this.food_preferences)) {
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
        for (let [, value] of Object.entries(this.food_preferences)) {
          if (value == false) return false;
        }
        return true;
      },
      set: function () {
        return false;
      },
    },
    relevantDishes: {
      get: function () {
        let relevantDishes = this.dishes.filter(
          (dish) =>
            // TODO: does not loop through all dish categories. Most have only one. This is just temporary solution for the demo 🫠
            // use a separate function (checkRelevance) instead - left to be finalized
            // this.checkRelevance(this.food_preferences, dishes.categories, "category") &
            // this.checkRelevance(this.allergies, dishes.dish.allergies, "allergy") &
            // this.checkRelevance(this.additives, dishes.dish.additives, "additive")
            this.food_preferences[dish.dish.categories[0].name]
          // & ! this.food_preferences[dish.dish.allergies[0].allergy.name]
          // & dish.dish.allergies.length > 0 ? !this.food_preferences[dish.dish.allergies[0].allergy.name] : true
          // & dish.dish.additives.length > 0 ? !this.food_preferences[dish.dish.additives[0].additive.name] : true
        );
        return relevantDishes;
      },
      set: function () {
        return this.dishes;
      },
    },
  },
  methods: {
    // import Register action
    ...mapActions(["Register"]),
    encrypt(m) {
      if (process.env.VUE_APP_PRIVATE_KEY) {
        let encryptor = new JSEncrypt();
        encryptor.setPublicKey(this.publicKey);
        return encryptor.encrypt(m);
      } else {
        return m;
      }
    },
    initialize_dish_ratings() {
      this.dish_ratings = [
        { id: null, rating: null },
        { id: null, rating: null },
        { id: null, rating: null },
      ];
    },
    initialize_dishes() {
      axios
        .post("api/v1/mensa/get_quiz_dishes", {
          categories: this.selected_categories,
          allergies: this.selected_allergies,
        })
        .then((response) => {
          var data = response.data;

          for (var i = 0; i < data.length; i++) {
            Vue.set(this.dishes, i, data[i]);
          }

          console.log(this.dishes);
        });
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
    updateSelectedCategories() {
      // Object.entries(this.food_preferences).forEach((key, value) =>
      for (const [key, value] of Object.entries(this.food_preferences)) {
        if (value) {
          this.selected_categories.push(key);
        }
      }
      this.initialize_dishes();
    },
    // TODO: To be finalized
    // checkRelevance(user_attribute, dish_attribute, attribute_name){
    //     for(let idx = 0; idx < dishes.length; idx++){
    //         attribute = String(dish_attribute[idx])+"."+attribute_name + ".name"
    //         console.log(attribute)
    //         console.log(user_attribute[attribute])
    //         if(!user_attribute[attribute]) return false
    //     }
    //     return true
    // },
    addRating(index, dish_id, rating) {
      this.dish_ratings[index] = { id: dish_id, rating: rating };
      if (this.cur_step_dishes < 3) {
        this.cur_step_dishes++;
      }
      // update to consider updated rating data
      this.$forceUpdate();
    },
    async register() {
      try {
        let User = {
          username: this.form.email,
          password: this.encrypt(this.form.password),
          card_id: this.form.mensa_card_id ? this.form.mensa_card_id : -1,
          categories: this.selected_categories,
          allergies: this.selected_allergies,
          ratings: this.dish_ratings,
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
  },
  created() {
    this.initialize_dish_ratings();
  },
};
</script>
