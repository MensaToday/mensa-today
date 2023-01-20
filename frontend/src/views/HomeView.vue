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
           
                    v-img(style="border-top-left-radius: 1%; border-top-right-radius: 1%" v-show="item[0].dish.url != null" :alt="item[0].dish.name" height='250'
                    :src='item[0].dish.url')
                    v-card.center-items.light-green.lighten-2(style="border-bottom-left-radius: 0%; border-bottom-right-radius: 0%" v-show="item[0].dish.url == null" height='250' elevation="0")
                      h1 {{ item[0].dish.name[0] }}
                    v-progress-linear(:height="6" :background-opacity=".5" :value="item[1]*100" )

                    v-card-title(style="line-height:1.2; font-size: 17px; word-break: normal; height:90px; overflow: hidden; white-space: pre-line;") {{ item[0].dish.name }}
                    //- v-card-subtitle.mt-1(:class="{'red--text': $store.state.card_balance <= (parseFloat(item[0].priceStudent)+1) }") €{{ item[0].priceStudent.replace('.',',') }}/{{ item[0].priceEmployee.replace('.',',') }} 
                    
                    v-divider
                    //- v-card-subtitle.mt-1(:class="{'red--text': $store.state.card_balance <= (parseFloat(item[0].priceStudent)+1) }") €{{ item[0].priceStudent.replace('.',',') }}/{{ item[0].priceEmployee.replace('.',',') }}

                    v-card-text
                      v-row 
                        v-col.adjusted-padding-margin.d-flex.justify-space-between
                          div.d-flex.align-center(style="font-weight: bold; font-size: 17px;" :class="{'red--text': $store.state.card_balance <= (parseFloat(item[0].priceStudent)+1) }") €{{ item[0].priceStudent.replace('.',',') }}/{{ item[0].priceEmployee.replace('.',',') }}
                          v-btn(rounded :href="getGoogleMapsUrl(item[0].mensa.name)" target="_blank" rel="noopener noreferrer")
                            v-icon mdi-navigation-variant-outline
                            | {{ (item[0].mensa.name).replace('Bistro Katholische Hochschule', 'Bistro Katho.').replace('Bistro Oeconomicum','Oeconomicum') }}

                      v-row 
                        v-col.adjusted-padding-margin.d-flex.justify-space-between
                          v-icon mdi-shield-plus-outline
                          div.d-flex
                            v-img(v-for="(category, index) in item[0].dish.categories.length" :alt="item[0].dish.categories[index].category.name" height="40" max-width="40" contain :key="category"
                              :src="require('@/assets/dish_icons/food_preferences/'+item[0].dish.categories[index].category.name+'.png')")

                      v-row
                        v-col.adjusted-padding-margin.d-flex.justify-space-between
                          v-btn(width="100%") View Side Dishes
                       

                      v-row
                        v-col.adjusted-padding-margin.d-flex.justify-end
                          v-rating(v-model="ratingItems[Object.keys(items).indexOf(key)][index].rating" half-increments hover length="5" background-color="gray" size="24" 
                            @input="updateRating(Object.keys(items).indexOf(key), index, $event); setRating(item[0].dish.id, $event);")

                          
                    
                      //- v-row
                      //-   div.ma-2
                      //-     h4.text-right.subheading(:class="{'red--text': $store.state.card_balance <= (parseFloat(item[0].priceStudent)+1) }") €{{ item[0].priceStudent.replace('.',',') }}/{{ item[0].priceEmployee.replace('.',',') }}
                          
                      //-     v-btn(rounded :href="getGoogleMapsUrl(item[0].mensa.name)" target="_blank" rel="noopener noreferrer")
                      //-       v-icon mdi-navigation-variant-outline
                      //-       | {{ (item[0].mensa.name).replace('Bistro Katholische Hochschule', 'Bistro Katho.').replace('Bistro Oeconomicum','Oeconomicum') }}
                      //-   v-row 
                      //-     v-col
                      //-       v-col.align-center.justify-center.d-flex.justify-space-between
                    
                      //-         v-icon mdi-shield-plus-outline
                      //-         v-img(v-for="(category, index) in item[0].dish.categories.length" :alt="item[0].dish.categories[index].category.name" 
                      //-           height="40" max-width="40" contain :key="category"
                      //-           :src="require('@/assets/dish_icons/food_preferences/'+item[0].dish.categories[index].category.name+'.png')")
      
                      //-   v-row.align-center.justify-center.d-flex.justify-space-between
                      //-     v-col
                      //-       v-card-actions
                      //-         v-spacer
                      //-         span {{ item[0].ext_ratings.rating_avg }}
                      //-         v-rating(v-model="ratingItems[Object.keys(items).indexOf(key)][index].rating" half-increments hover length="5" background-color="gray" size="24" 
                      //-           @input="updateRating(Object.keys(items).indexOf(key), index, $event); setRating(item[0].dish.id, $event);")
            
                        
                      
</template>

<script>
import { mapActions } from "vuex";
import axios from "axios";
export default {
  name: "HomeWeekRecommendation",
  data() {
    return {
      hover: false,
      currentTab: 0,
      tab: null,
      ratingItems : [
      [{ id: null, rating: 0 }, { id: null, rating: 0 }, { id: null, rating: 0 }, { id: null, rating: 0 }],
      [{ id: null, rating: 0 }, { id: null, rating: 0 }, { id: null, rating: 0 }, { id: null, rating: 0 }],
      [{ id: null, rating: 0 }, { id: null, rating: 0 }, { id: null, rating: 0 }, { id: null, rating: 0 }],
      [{ id: null, rating: 0 }, { id: null, rating: 0 }, { id: null, rating: 0 }, { id: null, rating: 0 }],
      [{ id: null, rating: 0 }, { id: null, rating: 0 }, { id: null, rating: 0 }, { id: null, rating: 0 }],
      ],
      model: null,
      recommendationItemsTest: null,
      recommendationItems: this.$store.state.recommendations,
      recommendationItemsDaily: this.$store.state.dailyRecommendations,
      days: [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
      ],
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
    ...mapActions(["GetRecommendations", "GetOneRecommendation", "GetUserData", "GetUserRatings"]),
    convertDate(date){
      let old_date = new Date(date);
      var dd = String(old_date.getDate()).padStart(2, "0");
      var mm = String(old_date.getMonth() + 1).padStart(2, "0"); //January is 0!
      var yyyy = old_date.getFullYear();
      var weekday = this.days[old_date.getDay()-1]
      return(weekday + ", " + dd + "." + mm + "." + yyyy);
    },
    prev() {
            console.log(this.currentTab)
            if (this.currentTab === 0) return
            this.currentTab = this.currentTab - 1
        },
    next() {
        console.log(this.currentTab)
        if (this.currentTab === Object.keys(this.items).length-1) return
        this.currentTab = this.currentTab + 1
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
    updateRating(key, index, value){
      this.ratingItems[key][index].rating = value;
      console.log(this.ratingItems);
    },
    print(msg){
      console.log(msg);
    },
    getGoogleMapsUrl(mensaName) {
      const url = new URL("https://www.google.com/maps/dir/?api=1");
      url.searchParams.set("destination", mensaName);
      return url.toString();
    },
    async setRating(dish_id, rating) {
      let response = await axios.post("mensa/user_ratings", {
        dish_id: dish_id,
        rating: rating
      });
      console.log(response);
    },
    initializeRatings(){
    },
  },
  mounted() {
    // TODO: exchange with getRecommendations
    //this.getOneRecommendation();
    this.getRecommendations();
    this.getUserRatings();
    this.initializeRatings();
    this.getUserData();
    
  },
};
</script>

<style>

.adjusted-padding-margin {
  margin: 3px;
  padding: 3px;
}

</style>