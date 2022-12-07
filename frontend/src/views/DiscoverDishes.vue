<template lang="pug">
    div  
      v-container
        h1.text-center.my-6 Discover Dishes
        //- v-btn(@click="getRecommendations()") Get Recommendations
        v-row 
          v-col
            v-skeleton-loader(v-show="!loaded" :loading="!loaded" transition="fade-transition" type="card")
            template(v-if="loaded")
              v-data-iterator(:items='items' :items-per-page.sync='itemsPerPage' :page.sync='page' 
                :search='search' hide-default-footer 
                :sort-desc="sortDesc")
                //- TODO: searches only first layer of json (date, price)
                //- :sort-by='sortBy.toLowerCase()'
                template(v-slot:header)
                    v-toolbar.mb-1(color='primary' dark)
                        h3 All Dishes
                        v-spacer
                        v-text-field(v-model='search' clearable flat solo-inverted hide-details 
                        prepend-inner-icon='mdi-magnify' label='Search')
                        template(v-if='$vuetify.breakpoint.mdAndUp')
                        v-spacer
                        v-select(v-model='sortBy' flat solo-inverted hide-details :items='keys' 
                            prepend-inner-icon='mdi-filter-variant' label='Filter')
                template(v-slot:default='props')
                  v-row
                    v-col(v-for='item in props.items' :key="item.dish.id" cols='12' sm='6' md='6' lg='4')
                        v-card(height="100%")
                            v-img(v-show="item.dish.url != null" :alt="item.dish.name" height='250'
                            :src="item.dish.url")
                            div.center-items.light-green.lighten-2(v-show="item.dish.url == null" height='250')
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
                                        | {{ item.dish.main ? 'Main Dish' : 'Supplement' }}
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
                        //- Review & Comment Section
                        //- v-col.d-flex.justify-space-between.py-0
                        //-     v-rating(hover length="5" background-color="gray" 
                        //-         v-model="suggested_dish_rating")
                        //-     v-btn(@click="") 
                        //-         v-icon mdi-comment-outline
                        //-         | comment 
                template(v-slot:footer)
                  v-row.mt-2(align='center' justify='center')
                    span.grey--text Items Per Page
                    v-menu(offset-y)
                      template(v-slot:activator='{ on, attrs }')
                        v-btn.ml-2(dark text color='primary' v-bind='attrs' v-on='on')
                          | {{ itemsPerPage }}
                          v-icon mdi-chevron-down
                      v-list
                        v-list-item(v-for='(number, index) in itemsPerPageArray' :key='(number, index)' 
                          @click='updateItemsPerPage(number)')
                          v-list-item-title {{ number }}
                    v-spacer
                    span.mr-4.grey--text
                      | Page {{ page }} of {{ numberOfPages }}
                    v-btn.mr-1(fab dark color='primary' @click='formerPage')
                      v-icon mdi-chevron-left
                    v-btn.ml-1(fab dark color='primary' @click='nextPage')
                      v-icon mdi-chevron-right
              
                //- info button with ingredients
                //- browse section for all dishes on all days 
                //- -> filter out for day, location, food preference, allergies
                //- sort by rating
    </template>
    
    <script>
    import { mapActions } from "vuex";
    export default {
      name: "Discover",
      data() {
        return {
            // TODO: rating to be implemented
            // suggested_dish_rating: null,
            itemsPerPageArray: [3, 6, 9],
            search: "",
            filter: {},
            sortDesc: false,
            page: 1,
            itemsPerPage: 3,
            sortBy: "",
            // TODO: filters:
            food_preferences: {
                Vegan: false,
                Vegetarian: false,
                Pork: false,
                Beef: false,
                Poultry: false,
                Alcohol: false,
                Fish: false,
            },
            keys: [
                "dish.categories[0].category",
                "dish.main",
                "mensa.name",
                "date",
                "priceStudent",
            ],
        };
      },
      computed: {
        items: {
            get() {
                // let relevantDishes = this.$store.state.dishplan.filter(dish => {
                // // TODO: does not loop through all dish categories. Most have only one. This is just temporary solution for the demo 🫠
                // // use a separate function (checkRelevance) instead - left to be finalized
                // // this.checkRelevance(this.food_preferences, dishes.categories, "category") & 
                // // this.checkRelevance(this.allergies, dishes.dish.allergies, "allergy") &
                // // this.checkRelevance(this.additives, dishes.dish.additives, "additive")
                // this.food_preferences[dish.dish.categories[0].category.name] 
                // // & ! this.food_preferences[dish.dish.allergies[0].allergy.name]
                // // & ! this.food_preferences[dish.dish.additives[0].additive.name]
                // });
                // return relevantDishes
                return this.$store.state.dishplan;
            },
            set() {
                return this.$store.state.dishplan;
            }
        },
        loaded(){
          if (this.items != null) return true
          else return false
        },
        numberOfPages() {
          if (this.items) return Math.ceil(this.items.length / this.itemsPerPage);
          else return 1;
        },
        filteredKeys() {
          return this.keys.filter((key) => key !== "Name");
        },
      },
      methods: {
        ...mapActions(["GetDishplan", "GetRecommendations"]),

        nextPage() {
          if (this.page + 1 <= this.numberOfPages) this.page += 1;
        },
        formerPage() {
          if (this.page - 1 >= 1) this.page -= 1;
        },
        updateItemsPerPage(number) {
          this.itemsPerPage = number;
        },
        async getDishplan() {
          try {
            await this.GetDishplan();
          } catch (error) {
            console.log(error);
          }
        },
        async getRecommendations(){
            try {
                var request_data = JSON.stringify({day: "2022.12.06", entire_week: "False"})
                await this.GetRecommendations(request_data);
            } catch (error) {
                console.log(error);
            }
        },
        ratingAsFloat(ratingAsString) {
          return parseFloat(ratingAsString)
        },
        getGoogleMapsUrl(mensaName) {
            const url = new URL("https://www.google.com/maps/dir/?api=1");
            url.searchParams.set("destination", mensaName);
            return url.toString();
        },
      },
      mounted() {
        this.getRecommendations()
        // if items not set, query dishplan
        if(!this.items) this.getDishplan()
      }
    };
    </script>
    