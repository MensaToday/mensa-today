<template lang="pug">
div
  v-container
    h1.text-center.my-6 Your Mensa Week
    v-row 
      v-col
        v-skeleton-loader(v-show="!loaded" :loading="!loaded" transition="fade-transition" type="card")
        template(v-if="loaded")
              v-data-iterator(:items='items' hide-default-footer)
                template(v-slot:default='props')
                  v-row
                    v-col(v-for='(item, index) in props.items' :key="index" cols='12' sm='6' md='6' lg='4')
                      v-card(height="100%")
                          v-card-title.align-center {{ days[(new Date(item.date)).getDay()] }}
                          v-img(v-show="item.dish.url != null" :alt="item.dish.name" height='250'
                          :src="item.dish.url")
                          v-card.center-items.light-green.lighten-2.rounded-b-0(v-show="item.dish.url == null" height='250' elevation="0")
                              h1 {{ item.dish.name[0] }}
                          
                          v-card-title.subheading(style="word-break: normal")
                              | {{ item.dish.name }}
                          v-divider
                          v-col.align-center.justify-center.d-flex.justify-space-between.py-0
                              h4.ma-0.text-right.subheading(:class="{'red--text': $store.state.card_balance <= (parseFloat(item.priceStudent)+1) }")
                                  //- (:class="{ 'primary--text': sortBy === key }")
                                  | €{{ item.priceStudent.replace('.',',') }}/{{ item.priceEmployee.replace('.',',') }}
                              v-img(v-for="(category, index) in item.dish.categories.length" :alt="item.dish.categories[index].category.name" 
                                  height="50" max-width="50" contain :key="category"
                                  :src="require('@/assets/dish_icons/food_preferences/'+item.dish.categories[index].category.name+'.png')")
                              v-btn(rounded :href="getGoogleMapsUrl(item.mensa.name)" target="_blank" rel="noopener noreferrer")
                                  v-icon mdi-navigation-variant-outline
                                  | {{ (item.mensa.name).replace('Bistro Katholische Hochschule', 'Bistro Katho.').replace('Bistro Oeconomicum','Oeconomicum') }}
                          v-col.align-center.justify-center.d-flex.justify-space-between
                              div
                                  span
                                      //- (:class="{ 'primary--text': sortBy === key }")
                                      v-icon mdi-food-apple
                                      | {{ item.dish.main ? 'Main Dish' : 'Side Dish' }}
                              div 
                                  v-icon mdi-shield-plus-outline
                                  span
                                      //- (:class="{ 'primary--text': sortBy === key }")
                                      span(v-if="item.dish.additives.length == 0")  None
                                      span(v-for="additive in item.dish.additives" :key="additive.additive.name")  {{ additive.additive.name }}
                          v-col.align-center.justify-center.d-flex.justify-space-between
                              div 
                                  v-icon mdi-calendar
                                  span {{ new Date(item.date).toLocaleDateString('de-DE') }}
                              v-rating(hover length="5" background-color="gray" readonly size="24" half-increments 
                                v-model="parseFloat(item.ext_ratings.rating_avg) + 0.0")
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "HomeWeekRecommendation",
  data() {
    return {
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
      return this.$store.state.dailyRecommendations;
    },
    loaded() {
      // if (typeof this.items !== 'undefined') return true
      if (this.items != null) return true;
      else return false;
    },
  },
  methods: {
    ...mapActions(["GetRecommendations", "GetOneRecommendation"]),

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
  },
  mounted() {
    // TODO: exchange with getRecommendations
    this.getOneRecommendation();
    // this.getRecommendations()
  },
};
</script>
