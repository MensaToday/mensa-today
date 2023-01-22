<template lang="pug">
div
  v-container
    h1.text-center.my-6 Your Mensa Week
    v-row 
      v-col
        v-skeleton-loader(v-show="!loaded" :loading="!loaded" type="card")
        template(v-if="loaded")

          v-tabs(fixed-tabs v-model="tab")
            v-btn.elevation-0(tile style="border-bottom-left-radius: 25px; border-top-left-radius: 25px;" @click="prev();")
              v-icon mdi-chevron-left
            v-btn.elevation-0(tile style ="text-transform: unset !important" width="150px") {{ this.convertDate(Object.keys(items)[currentTab])  }}
            v-btn.elevation-0(tile style="border-bottom-right-radius: 25px; border-top-right-radius: 25px;" @click="next();")
              v-icon mdi-chevron-right

            v-tabs-slider(color="primary")

          v-tabs-items.align-center.justify-center.d-flex.py-2(v-model="tab") 
            template(v-for="(array, key) in items")
              template(v-if="currentTab === Object.keys(items).indexOf(key)")
                v-row.justify-center
                  v-card.ma-2(height="570px" width="350px" v-for="(item, index) in array" :key="index")

                    v-img(style="border-top-left-radius: 1%; border-top-right-radius: 1%" v-show="item.dish.url != null" :alt="item.dish.name" height='250'
                    :src='item.dish.url')
                    v-card.center-items.light-green.lighten-2(style="border-bottom-left-radius: 0%; border-bottom-right-radius: 0%" v-show="item.dish.url == null" height='250' elevation="0")
                      h1 {{ item.dish.name[0] }}
                    v-progress-linear(:height="6" :background-opacity=".5" :value="item[1]*100" )

                    v-card-title(style="line-height:1.2; font-size: 17px; word-break: normal; height:90px; overflow: hidden; white-space: pre-line;") 
                    | {{ item.dish.name }}

                    v-divider

                    v-card-text.mt-2
                      v-row
                        v-col.align-center.justify-center.d-flex.justify-space-between.py-0
                          h3.ma-0(:class="{'red--text': $store.state.card_balance ? $store.state.card_balance <= (parseFloat(item.priceStudent)+1) : false }")
                            | €{{ item.priceStudent.replace('.',',') }}/{{ item.priceEmployee.replace('.',',') }}
                          div
                            v-btn(fab small elevation="2" @click="selectCard(item); dish_overlay = true")
                              v-icon(color="primary") mdi-information-outline
                          div.d-flex
                            v-img(v-for="(category, index) in item.dish.categories.length" :alt="item.dish.categories[index].name" 
                              height="50" max-width="50" contain :key="category"
                              :src="require('@/assets/dish_icons/food_preferences/'+item.dish.categories[index].name+'.png')")
                      v-row
                        v-col.align-center.justify-center.d-flex.justify-space-between
                          span
                            v-icon.mr-2 mdi-food-apple 
                            | {{ item.dish.main ? 'Main' : 'Side' }}
                        v-col 
                          v-btn(rounded :href="getGoogleMapsUrl(item.mensa.name)" target="_blank" rel="noopener noreferrer")
                            v-icon mdi-navigation-variant-outline
                            | {{ (item.mensa.name).replace('Bistro Katholische Hochschule', 'Bistro Katho.').replace('Bistro Oeconomicum','Oeconomicum') }}
                      v-row
                        v-col.align-center.justify-center.d-flex.justify-space-between
                          div 
                            v-icon.mr-2 mdi-shield-plus-outline
                            span
                              (:class="{ 'primary--text': sortBy === key }")
                              span(v-if="item.dish.additives.length == 0") None
                              span(v-for="additive in item.dish.additives" :key="additive.name") 
                                span {{ additive.name }}
                                span(v-show="additive != item.dish.additives[item.dish.additives.length-1]") , 
                          div 
                            v-icon.mr-2 mdi-calendar
                            span {{ new Date(item.date).toLocaleDateString('de-DE') }}
                      v-row
                        v-col.align-center.justify-center.d-flex.justify-space-between
                          div
                            v-icon.mr-2 mdi-thumbs-up-down-outline
                            span(v-if="item.ext_ratings.rating_count != 0") {{ item.ext_ratings.rating_avg }}
                            span(v-else) No ratings
                          //- v-rating(v-model="ratingItems[Object.keys(items).indexOf(key)][index].rating" half-increments hover length="5" background-color="gray" size="24" 
                          //-   @input="updateRating(Object.keys(items).indexOf(key), index, $event); setRating(item.dish.id, $event);")

          //- Overlay for Selected Dish
          v-dialog(absolute :value="dish_overlay" transition="dialog-bottom-transition" color="primary" width="95%")
            v-btn(fixed top right color="primary" fab small @click="dish_overlay = false")
              v-icon mdi-close
            //- only try to render if a dish is selected
            v-card.center-items(v-if="dish_overlay")
              v-row
                v-col.align-center.justify-center.d-flex.justify-space-around
                  v-card.center-items(color="transparent" flat)
                    v-card-title 
                      h2.my-3 Dish Combination
                    v-card-text 
                      v-row
                        v-col.align-center.justify-center.d-flex.justify-space-around
                          v-btn(rounded :href="getGoogleMapsUrl(selected_dish.mensa.name)" target="_blank" rel="noopener noreferrer")
                            v-icon mdi-navigation-variant-outline
                            | {{ (selected_dish.mensa.name).replace('Bistro Katholische Hochschule', 'Bistro Katho.').replace('Bistro Oeconomicum','Oeconomicum') }}
                          div.ml-4
                            v-icon.mr-2 mdi-calendar
                            span {{ new Date(selected_dish.date).toLocaleDateString('de-DE') }}
              v-row(no-gutters)
                v-col.align-center.justify-center(cols="12" md="4")
                  h3.text-center.my-3 Main Dishes
                  DishCard(:dish="selected_dish" fixed :card_width="'20vw'")
                v-col.center-items(cols="12" md="8")
                  v-card.center-items.pa-3(v-if="selected_dish.side_dishes.length == 0" color="grey")
                    h3.my-0 No suggested side dishes
                  div.center-items(v-else)
                    h3.my-3 Side Dishes
                    .d-flex.flex-wrap
                      DishCard(:dish="side_dish" :side_dish="true" :card_width="'15vw'" v-for="side_dish in selected_dish.side_dishes" :key="side_dish.dish.name")
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";
import DishCard from "../components/DishCard.vue";
export default {
  name: "HomeWeekRecommendation",
  components: { DishCard },
  data() {
    return {
      hover: false,
      currentTab: 0,
      tab: null,
      ratingItems: [
        [
          { id: null, rating: 0 },
          { id: null, rating: 0 },
          { id: null, rating: 0 },
          { id: null, rating: 0 },
        ],
        [
          { id: null, rating: 0 },
          { id: null, rating: 0 },
          { id: null, rating: 0 },
          { id: null, rating: 0 },
        ],
        [
          { id: null, rating: 0 },
          { id: null, rating: 0 },
          { id: null, rating: 0 },
          { id: null, rating: 0 },
        ],
        [
          { id: null, rating: 0 },
          { id: null, rating: 0 },
          { id: null, rating: 0 },
          { id: null, rating: 0 },
        ],
        [
          { id: null, rating: 0 },
          { id: null, rating: 0 },
          { id: null, rating: 0 },
          { id: null, rating: 0 },
        ],
      ],
      model: null,
      recommendationItemsTest: null,
      recommendationItems: this.$store.state.recommendations,
      recommendationItemsDaily: this.$store.state.dailyRecommendations,
      days: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      dish_overlay: false,
      selected_dish: null,
    };
  },
  computed: {
    userRatings() {
      return this.$store.state.user.user_ratings;
    },
    items() {
      return this.$store.state.recommendations;
    },
    itemLabels() {
      return Object.keys(this.$store.state.recommendations);
    },
    loaded() {
      // if (typeof this.items !== 'undefined') return true
      if (this.items != null) return true;
      else return false;
    },
  },
  methods: {
    ...mapActions([
      "GetRecommendations",
      "GetOneRecommendation",
      "GetUserData",
      "GetUserRatings",
    ]),
    convertDate(date) {
      let dd = date.slice(8, 10);
      let mm = date.slice(5, 7);
      let yyyy = date.slice(0, 4);
      var str = mm + "/" + dd + "/" + yyyy;
      var dateObject = new Date(str);
      let weekday = this.days[dateObject.getDay() - 1];

      return weekday + ", " + dd + "." + mm + "." + yyyy;
    },
    prev() {
      if (this.currentTab === 0) return;
      this.currentTab = this.currentTab - 1;
    },
    next() {
      if (this.currentTab === Object.keys(this.items).length - 1) return;
      this.currentTab = this.currentTab + 1;
    },
    selectCard(item) {
      this.dish_overlay = true;
      this.selected_dish = item;
    },
    async getUserRatings() {
      try {
        await this.GetUserRatings();
      } catch (error) {
        console.log(error);
      }
    },
    async getUserData() {
      try {
        await this.GetUserData();
      } catch (error) {
        console.log(error);
      }
    },
    async getRecommendations() {
      try {
        await this.GetRecommendations();
      } catch (error) {
        console.log(error);
      }
    },
    async getOneRecommendation() {
      try {
        await this.GetOneRecommendation();
      } catch (error) {
        console.log(error);
      }
    },
    onCardClick(event) {
      event.preventDefault();
    },
    updateRating(key, index, value) {
      this.ratingItems[key][index].rating = value;
      // console.log(this.ratingItems);
    },
    getGoogleMapsUrl(mensaName) {
      const url = new URL("https://www.google.com/maps/dir/?api=1");
      url.searchParams.set("destination", mensaName);
      return url.toString();
    },
    async setRating(dish_id, rating) {
      let response = await axios.post("mensa/user_ratings", {
        dish_id: dish_id,
        rating: rating,
      });
      console.log(response);
    },
  },
  mounted() {
    this.getRecommendations();
    this.getUserRatings();
    // this.initializeRatings();
    this.getUserData();
  },
};
</script>
