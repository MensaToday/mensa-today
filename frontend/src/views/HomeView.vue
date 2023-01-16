<template lang="pug">
div
  v-container
    h1.text-center.my-6 Your Mensa Week
    v-row 
      v-col
        v-skeleton-loader(v-show="!loaded" :loading="!loaded" type="card")
        template(v-if="loaded")
          div.pb-4(v-for="(array, key) in items" :key="key")
            v-sheet.mx-auto.elevation-4(max-width="1600")
              div
                //- h4.mx-auto Hi
                v-slide-group.pa-2(show-arrows)
                  v-slide-item(v-for="(item, index) in array" :key="index" )
                    
                    v-card.pa-4(height="650" width="500")
                      v-img(v-show="item[0].dish.url != null" :alt="item[0].dish.name" height='300'
                      :src='item[0].dish.url')
                        //- v-progress-circular(:rotate="-90" :size="100" :width="15" :value="item[1]*100" color="primary") {{ (item[1]*100).toFixed(2) }}

                      v-card.center-items.light-green.lighten-2.rounded-b-0(v-show="item[0].dish.url == null" height='300' elevation="0")
                        h1 {{ item[0].dish.name[0] }}
                        
                      v-card-title(style="font-size: 17px; word-break: normal; height:90px; overflow: hidden; white-space: pre-line;") {{ item[0].dish.name }}

                      v-divider

                      v-col.align-center.justify-center.d-flex.justify-space-between.py-2
                        h4.ma-0.text-right.subheading(:class="{'red--text': $store.state.card_balance <= (parseFloat(item[0].priceStudent)+1) }") €{{ item[0].priceStudent.replace('.',',') }}/{{ item[0].priceEmployee.replace('.',',') }}
                        
                        v-btn(rounded :href="getGoogleMapsUrl(item[0].mensa.name)" target="_blank" rel="noopener noreferrer")
                          v-icon mdi-navigation-variant-outline
                          | {{ (item[0].mensa.name).replace('Bistro Katholische Hochschule', 'Bistro Katho.').replace('Bistro Oeconomicum','Oeconomicum') }}

                      v-col.align-center.justify-center.d-flex.justify-space-between

                        div
                          v-img(v-for="(category, index) in item[0].dish.categories.length" :alt="item[0].dish.categories[index].category.name" 
                            height="50" max-width="50" contain :key="category"
                            :src="require('@/assets/dish_icons/food_preferences/'+item[0].dish.categories[index].category.name+'.png')")
                          //- span
                          //-   //- (:class="{ 'primary--text': sortBy === key }")
                          //-   v-icon mdi-food-apple
                          //-   | {{ item[0].dish.main ? 'Main Dish' : 'Side Dish' }}
                      
                        div 
                          v-icon mdi-shield-plus-outline
                          span
                            //- (:class="{ 'primary--text': sortBy === key }")
                            span(v-if="item[0].dish.additives.length == 0")  None
                            span(v-for="additive in item[0].dish.additives" :key="additive.additive.name")  {{ additive.additive.name }}
                     
                      v-col.align-center.justify-center.d-flex.justify-space-between
                        v-spacer
                        span {{ item[0].ext_ratings.rating_avg }}
                        v-rating(v-model="rating" half-increments hover length="5" background-color="gray" readonly size="24" 
                          :value="parseFloat(item[0].ext_ratings.rating_avg) + 0.0")
                        v-btn(@click="setRating(item[0].dish.id, 5)")
        
</template>

<script>
import { mapActions } from "vuex";
import { axios } from "axios";
export default {
  name: "HomeWeekRecommendation",
  data() {
    return {
      rating: 0.0,
      model: null,
      recommendationItemsTest: null,
      recommendationItems: this.$store.state.recommendations,
      recommendationItemsDaily: this.$store.state.dailyRecommendations,
      days: [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      ],
    };
  },
  computed: {
    items() {
      return this.$store.state.recommendations;
    },
    loaded() {
      // if (typeof this.items !== 'undefined') return true
      if (this.items != null) return true;
      else return false;
    },
  },
  methods: {
    ...mapActions(["GetRecommendations", "GetOneRecommendation"]),
    print(msg){
      console.log(msg);
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
    }
  },
  mounted() {
    // TODO: exchange with getRecommendations
    //this.getOneRecommendation();
    this.getRecommendations();
  },
};
</script>

