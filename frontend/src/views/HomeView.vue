<template lang="pug">
div
  v-container
    h1.text-center.my-6 Your Mensa Week
    div(:class="$vuetify.breakpoint.mdAndUp ? 'float-right' : 'd-flex mb-3 justify-center'")
      v-btn(v-show="dayViewSelected==false" @click="dayViewSelected=true" rounded) 
        v-icon mdi-view-week-outline
        | Week View 
      v-btn(v-show="dayViewSelected==true" @click="dayViewSelected=false" rounded) 
        v-icon mdi-view-day-outline
        | Day View 
    v-row 
      v-col
        //- Day View
        v-skeleton-loader(v-show="!dailyRecommendationLoaded" :loading="!dailyRecommendationLoaded" type="card")
        template(v-if="dailyRecommendationLoaded && dayViewSelected")
          v-tabs(fixed-tabs v-model="tab")
            v-btn.elevation-0(tile @click="prev();"
              style="border-bottom-left-radius: 25px; border-top-left-radius: 25px;")
              v-icon mdi-chevron-left
            v-btn.elevation-0(tile style ="text-transform: unset !important" width="150px") 
              | {{ this.convertDate(Object.keys(items)[currentTab]) }}
            v-btn.elevation-0(tile @click="next();"
              style="border-bottom-right-radius: 25px; border-top-right-radius: 25px;")
              v-icon mdi-chevron-right

            v-tabs-slider(color="primary")

          v-tabs-items.align-center.justify-center.d-flex.py-2(v-model="tab") 
            h3(v-show="items[Object.keys(items)[currentTab]].length == 0") There are no recommended dishes today. The mensa might be closed.
            template(v-for="(array, key) in items")
              template(v-if="currentTab === Object.keys(items).indexOf(key)")
                v-row.justify-center
                  v-card.ma-2(width="350px" v-for="(item, index) in array" :key="index")
                    v-img(
                    v-show="item[0].dish.url != null" :alt="item[0].dish.name" 
                    height='250' :src='item[0].dish.url')
                    v-card.center-items.light-green.lighten-2(
                      style="border-bottom-left-radius: 0%; border-bottom-right-radius: 0%" 
                      v-show="item[0].dish.url == null" height='250' elevation="0")
                      h1 {{ item[0].dish.name[0] }}
                    v-tooltip(bottom)
                      template(v-slot:activator="{ on, attrs }")
                        v-progress-linear(v-bind="attrs" v-on="on" :height="6" :background-opacity=".5" :value="item[1]*100" )
                      span Recommendation: {{(item[1]*100).toFixed(0) }}%

                    v-card-title(height="90"
                      style="line-height:1.2; font-size: 17px; word-break: normal;overflow: hidden; white-space: pre-line;") 
                      | {{ item[0].dish.name }}

                    v-divider

                    v-card-text.mt-2
                      v-row
                        v-col.align-center.d-flex.justify-space-between.py-0
                          h3.ma-0(
                            :class="coveredByBalance(parseFloat(item.priceStudent))")
                            | €{{ item[0].priceStudent.replace('.',',') }}/{{ item[0].priceEmployee.replace('.',',') }}
                          div.d-flex
                            v-img(v-for="(category, index) in item[0].dish.categories.length" 
                              :alt="item[0].dish.categories[index].name" 
                              height="50" max-width="50" contain :key="category"
                              :src="require('@/assets/dish_icons/food_preferences/'+item[0].dish.categories[index].name+'.png')")
                      v-row
                        v-col.align-center.d-flex.justify-space-between
                          span
                            v-icon.mr-2 mdi-food-apple 
                            | {{ item[0].dish.main ? 'Main' : 'Side' }}
                        v-col 
                          v-btn.text-none(rounded :href="getGoogleMapsUrl(item[0].mensa.name)" target="_blank" rel="noopener noreferrer")
                            v-icon mdi-navigation-variant-outline
                            | {{ (item[0].mensa.name).replace('Bistro Katholische Hochschule', 'Bistro Katho.').replace('Bistro Oeconomicum','Oeconomicum') }}
                      v-row
                        v-col.align-center.d-flex.justify-space-between
                          div 
                            v-icon.mr-2 mdi-shield-plus-outline
                            span
                              span(v-if="item[0].dish.additives.length == 0") None
                              span(v-for="additive in item[0].dish.additives" :key="additive.name") 
                                span {{ additive.name }}
                                span(v-show="additive != item[0].dish.additives[item[0].dish.additives.length-1]") , 
                          div 
                            v-icon.mr-2 mdi-calendar
                            span {{ new Date(item[0].date).toLocaleDateString('de-DE') }}
                      v-row
                        v-col.align-center.d-flex.justify-space-between
                          div
                            v-icon.mr-2 mdi-thumbs-up-down-outline
                            span(v-if="item[0].ext_ratings.rating_count != 0") {{ item[0].ext_ratings.rating_avg }}
                            span(v-else) No ratings
                          v-rating(v-if = "item[0].user_ratings.length > 0" :value = "item[0].user_ratings[0].rating*5" hover length="5" background-color="gray" size="24" 
                            @input="setRating(item[0].dish.id, $event);")
                          v-rating(v-else hover length="5" background-color="gray" size="24" 
                            @input="setRating(item[0].dish.id, $event);")

                      v-divider
                      v-row
                        v-col.d-flex.justify-space-between.pb-0
                          h4.my-3 Selected Side Dishes
                          v-btn.mt-1(fab small elevation="2" outlined color="primary" :height="side_dish_icon_height" :width="side_dish_icon_height"
                            @click="selectCard(item[0]); dish_overlay = true")
                            v-icon(color="primary") mdi-plus
                      v-row
                        v-col.pt-0
                          template(v-for='(side_dish, i) in item[0].side_dishes')
                            v-divider(v-if='!side_dish' :key='`divider-${i}`')
                            div.d-flex.justify-space-between(v-else-if="side_dish.side_selected")
                              div.d-flex.flex-row
                                v-img.mr-1(v-for="(category, index) in side_dish.dish.categories.length" :alt="side_dish.dish.categories[index].name" 
                                  :height="category_icon_height" :max-width="category_icon_height" contain :key="category"
                                  :src="require('@/assets/dish_icons/food_preferences/'+side_dish.dish.categories[index].name+'.png')")
                                p.mb-0(:key='`item-${i}`') {{ side_dish.dish.name }}
                              p.ma-0.subheading(
                                :class="coveredByBalance(parseFloat(side_dish.priceStudent)+parseFloat(item[0].priceStudent))")
                                | €{{ side_dish.priceStudent.replace('.',',') }}/{{ side_dish.priceEmployee.replace('.',',') }}

          //- Overlay for Selected Dish
          v-dialog(absolute :value="dish_overlay" transition="dialog-bottom-transition" 
            color="primary" :width="$vuetify.breakpoint.mdAndUp ? '40vw' : '90vw'" 
            @click:outside="resetSelection();")
            //- only try to render if a dish is selected
            v-card.pt-4(v-if="dish_overlay" width="100%")
              h3.my-4.text-center(v-if="selected_dish.side_dishes.length == 0") No suggested side dishes
              template.center-items(v-else)
                v-list(shaped)
                  v-list-item-group(v-model='selected_side_dishes' multiple)
                    h3.my-3.text-center Side Dishes
                    template(v-for='(side_dish, i) in selected_dish.side_dishes')
                      v-divider(v-if='!side_dish' :key='`divider-${i}`')
                      v-list-item(v-else :key='`item-${i}`' :value='side_dish' active-class='primary--text text--accent-4')
                        template(v-slot:default='{ active }')
                          v-list-item-action
                            v-checkbox(:input-value='active' color='primary accent-4')
                          v-list-item-content
                            v-list-item-title 
                              h4.my-1 {{ side_dish.dish.name }}
                            div.d-flex.flex-row.center-items
                              p.ma-0.mr-3.text-right.subheading(
                                :class="coveredByBalance(parseFloat(side_dish.priceStudent)+parseFloat(selected_dish.priceStudent))")
                                | €{{ side_dish.priceStudent.replace('.',',') }}/{{ side_dish.priceEmployee.replace('.',',') }}
                              v-img(v-for="(category, index) in side_dish.dish.categories.length" :alt="side_dish.dish.categories[index].name" 
                                :height="category_icon_height" :max-width="category_icon_height" contain :key="category"
                                :src="require('@/assets/dish_icons/food_preferences/'+side_dish.dish.categories[index].name+'.png')")
                          v-list-item-icon(v-if='selected_dish.popular_side.id==side_dish.id' :right="true")
                            v-icon(color="#FFD700") mdi-star
              v-card-actions
                v-btn(@click="resetSelection(); dish_overlay = false")
                  v-icon.mr-2 mdi-close
                  | Cancel
                v-spacer
                v-btn(color="primary" @click="updateSelectedSideDishes(); dish_overlay = false"
                  v-show="selected_dish.side_dishes.length != 0")
                  v-icon.mr-2 mdi-check
                  | Save

        //- Week Overview
        template(v-if="weekRecommendationLoaded && !dayViewSelected")
          v-row.justify-center
            v-card.ma-2(width="350px" v-for="(item, index) in weekRecommendation" :key="index")
              v-card-title.my-0.text-center {{ days[index] }}
              //- p {{ item.dish }}
              h3.pa-3.text-center(v-if="Object.keys(item).length == 0") There are no recommended dishes today
              div(v-else)
                v-img(
                v-show="item.dish.url != null" :alt="item.dish.name" 
                height='250' :src='item.dish.url')
                v-card.center-items.light-green.lighten-2(
                  style="border-radius: 0%;" 
                  v-show="item.dish.url == null" height='250' elevation="0")
                  h1 {{ item.dish.name[0] }}
                v-tooltip(bottom)
                  template(v-slot:activator="{ on, attrs }")
                    v-progress-linear(v-bind="attrs" v-on="on" :height="6" :background-opacity=".5" :value="item[1]*100" )
                  span Recommendation: {{(item[1]*100).toFixed(0) }}%

                v-card-title(height="90"
                  style="line-height:1.2; font-size: 17px; word-break: normal;overflow: hidden; white-space: pre-line;") 
                  | {{ item.dish.name }}

                v-divider

                v-card-text.mt-2
                  v-row
                    v-col.align-center.d-flex.justify-space-between.py-0
                      h3.ma-0(
                        :class="coveredByBalance(parseFloat(item.priceStudent))")
                        | €{{ item.priceStudent.replace('.',',') }}/{{ item.priceEmployee.replace('.',',') }}
                      div.d-flex
                        v-img(v-for="(category, index) in item.dish.categories.length" 
                          :alt="item.dish.categories[index].name" 
                          height="50" max-width="50" contain :key="category"
                          :src="require('@/assets/dish_icons/food_preferences/'+item.dish.categories[index].name+'.png')")
                  v-row
                    v-col.align-center.d-flex.justify-space-between
                      span
                        v-icon.mr-2 mdi-food-apple 
                        | {{ item.dish.main ? 'Main' : 'Side' }}
                    v-col 
                      v-btn.text-none(rounded :href="getGoogleMapsUrl(item.mensa.name)" target="_blank" rel="noopener noreferrer")
                        v-icon mdi-navigation-variant-outline
                        | {{ (item.mensa.name).replace('Bistro Katholische Hochschule', 'Bistro Katho.').replace('Bistro Oeconomicum','Oeconomicum') }}
                  v-row
                    v-col.align-center.d-flex.justify-space-between
                      div 
                        v-icon.mr-2 mdi-shield-plus-outline
                        span
                          span(v-if="item.dish.additives.length == 0") None
                          span(v-for="additive in item.dish.additives" :key="additive.name") 
                            span {{ additive.name }}
                            span(v-show="additive != item.dish.additives[item.dish.additives.length-1]") , 
                      div 
                        v-icon.mr-2 mdi-calendar
                        span {{ new Date(item.date).toLocaleDateString('de-DE') }}
                  v-row
                    v-col.align-center.d-flex.justify-space-between
                      div
                        v-icon.mr-2 mdi-thumbs-up-down-outline
                        span(v-if="item.ext_ratings.rating_count != 0") {{ item.ext_ratings.rating_avg }}
                        span(v-else) No ratings
                      v-rating(v-if = "item.user_ratings.length > 0" :value = "item.user_ratings[0].rating*5" hover length="5" background-color="gray" size="24" 
                        @input="setRating(item.dish.id, $event);")
                      v-rating(v-else hover length="5" background-color="gray" size="24" 
                        @input="setRating(item.dish.id, $event);")

                  v-divider
                  v-row
                    v-col.d-flex.justify-space-between.pb-0
                      h4.my-3 Selected Side Dishes
                      v-btn.mt-1(fab small elevation="2" outlined color="primary" :height="side_dish_icon_height" :width="side_dish_icon_height"
                        @click="selectCard(item); dish_overlay = true")
                        v-icon(color="primary") mdi-plus
                  v-row
                    v-col.pt-0
                      template(v-for='(side_dish, i) in item.side_dishes')
                        v-divider(v-if='!side_dish' :key='`divider-${i}`')
                        div.d-flex.justify-space-between(v-else-if="side_dish.side_selected")
                          div.d-flex.flex-row
                            v-img.mr-1(v-for="(category, index) in side_dish.dish.categories.length" :alt="side_dish.dish.categories[index].name" 
                              :height="category_icon_height" :max-width="category_icon_height" contain :key="category"
                              :src="require('@/assets/dish_icons/food_preferences/'+side_dish.dish.categories[index].name+'.png')")
                            p.mb-0(:key='`item-${i}`') {{ side_dish.dish.name }}
                          p.ma-0.subheading(
                            :class="coveredByBalance(parseFloat(side_dish.priceStudent)+parseFloat(item.priceStudent))")
                            | €{{ side_dish.priceStudent.replace('.',',') }}/{{ side_dish.priceEmployee.replace('.',',') }}

          //- TODO: make code cleaner by extracting dialog into separate component
          //- Overlay for Selected Dish
          v-dialog(absolute :value="dish_overlay" transition="dialog-bottom-transition" 
            color="primary" :width="$vuetify.breakpoint.mdAndUp ? '40vw' : '90vw'" 
            @click:outside="resetSelection();")
            //- only try to render if a dish is selected
            v-card.pt-4(v-if="dish_overlay" width="100%")
              h3.my-4.text-center(v-if="selected_dish.side_dishes.length == 0") No suggested side dishes
              template.center-items(v-else)
                v-list(shaped)
                  v-list-item-group(v-model='selected_side_dishes' multiple)
                    h3.my-3.text-center Side Dishes
                    template(v-for='(side_dish, i) in selected_dish.side_dishes')
                      v-divider(v-if='!side_dish' :key='`divider-${i}`')
                      v-list-item(v-else :key='`item-${i}`' :value='side_dish' active-class='primary--text text--accent-4')
                        template(v-slot:default='{ active }')
                          v-list-item-action
                            v-checkbox(:input-value='active' color='primary accent-4')
                          v-list-item-content
                            v-list-item-title 
                              h4.my-1 {{ side_dish.dish.name }}
                            div.d-flex.flex-row.center-items
                              p.ma-0.mr-3.text-right.subheading(
                                :class="coveredByBalance(parseFloat(side_dish.priceStudent)+parseFloat(selected_dish.priceStudent))")
                                | €{{ side_dish.priceStudent.replace('.',',') }}/{{ side_dish.priceEmployee.replace('.',',') }}
                              v-img(v-for="(category, index) in side_dish.dish.categories.length" :alt="side_dish.dish.categories[index].name" 
                                :height="category_icon_height" :max-width="category_icon_height" contain :key="category"
                                :src="require('@/assets/dish_icons/food_preferences/'+side_dish.dish.categories[index].name+'.png')")
                          v-list-item-icon(v-if='selected_dish.popular_side.id==side_dish.id' :right="true")
                            v-icon(color="#FFD700") mdi-star
              v-card-actions
                v-btn(@click="resetSelection(); dish_overlay = false")
                  v-icon.mr-2 mdi-close
                  | Cancel
                v-spacer
                v-btn(color="primary" @click="updateSelectedSideDishes(); dish_overlay = false"
                  v-show="selected_dish.side_dishes.length != 0")
                  v-icon.mr-2 mdi-check
                  | Save      
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
      dayViewSelected: false,
      currentTab: 0,
      tab: null,
      days: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      dish_overlay: false,
      selected_dish: null,
      selected_side_dishes: [],
      category_icon_height: "20px",
      side_dish_icon_height: "36px",
    };
  },
  computed: {
    userRatings() {
      return this.$store.state.user.user_ratings;
    },
    items() {
      return this.$store.state.recommendations;
    },
    weekRecommendation() {
      return this.$store.state.dailyRecommendations;
    },
    dailyRecommendationLoaded() {
      if (this.items != null) return true;
      else return false;
    },
    weekRecommendationLoaded() {
      // todo save daily recommendations where?
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
      "SaveUserSideDishes",
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
    coveredByBalance(price) {
      if (!this.$store.state.card_balance) return null;
      if (this.$store.state.card_balance <= price) return "red--text";
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
      let selected_side_dishes_temp = [];
      item.side_dishes.forEach((side_dish) => {
        if (side_dish.side_selected == true) {
          selected_side_dishes_temp.push(side_dish);
        }
      });

      this.selected_side_dishes = selected_side_dishes_temp;
    },
    resetSelection() {
      this.selected_dish = null;
      this.dish_overlay = false;
      this.selected_side_dishes = [];
    },
    async updateSelectedSideDishes() {
      // loop through the side dishes of the selected dish
      // this.selected_dish.side_dishes = side dishes of selected card presented in v-dialog
      // this.selected_side_dishes = array of side dishes that are selected; subset of this.selected_dish.side_dishes
      if (this.selected_side_dishes.length != 0) {
        for (let idx = 0; idx < this.selected_dish.side_dishes.length; idx++) {
          let cur_side_dish_id = this.selected_dish.side_dishes[idx].dish.id;
          const selected_length = this.selected_side_dishes.length;
          for (let idx_select = 0; idx_select < selected_length; idx_select++) {
            let cur_selected_side_dish_id =
              this.selected_side_dishes[idx_select].dish.id;
            // if item matches any item from the temporary variable selected_side_dishes, it is updated as selected
            if (cur_side_dish_id == cur_selected_side_dish_id) {
              this.selected_dish.side_dishes[idx].side_selected = true;
              break;
            }
            // else it is marked as not selected (=deselected)
            else if ((idx_select += 1 == selected_length))
              this.selected_dish.side_dishes[idx].side_selected = false;
          }
        }
      } else {
        for (let idx = 0; idx < this.selected_dish.side_dishes.length; idx++) {
          this.selected_dish.side_dishes[idx].side_selected = false;
        }
      }

      try {
        let date = Object.keys(this.items)[this.currentTab];
        await this.SaveUserSideDishes([
          date,
          this.selected_dish.id,
          this.selected_dish.side_dishes,
        ]);
      } catch (error) {
        console.log(error);
      }
      this.resetSelection();
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
    getGoogleMapsUrl(mensaName) {
      const url = new URL("https://www.google.com/maps/dir/?api=1");
      url.searchParams.set("destination", mensaName);
      return url.toString();
    },
    async setRating(dish_id, rating) {
      await axios.post("mensa/user_ratings", {
        dish_id: dish_id,
        rating: rating,
      });
    },
  },
  mounted() {
    this.getOneRecommendation();
    this.getRecommendations();
    this.getOneRecommendation();
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
