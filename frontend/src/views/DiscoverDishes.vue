<template lang="pug">
    div  
      v-container
        h1.text-center.my-6 Discover Dishes
        v-row 
          v-col
            v-skeleton-loader(v-show="!loaded" :loading="!loaded" transition="fade-transition" type="card")
            template(v-if="loaded")
              v-data-iterator(:items='items' :items-per-page.sync='itemsPerPage' :page.sync='page' 
                :search='search' :sort-by='sortBy.toLowerCase()' hide-default-footer)
                template(v-slot:header)
                  v-toolbar.mb-1(color='primary' dark)
                    h3 Dishes for {{ $store.state.dishplan[0].date }} 
                    v-spacer
                    v-text-field(v-model='search' clearable flat solo-inverted hide-details 
                      prepend-inner-icon='mdi-magnify' label='Search')
                    template(v-if='$vuetify.breakpoint.mdAndUp')
                      v-spacer
                      v-select(v-model='sortBy' flat solo-inverted hide-details :items='keys' 
                        prepend-inner-icon='mdi-filter-variant' label='Filter')
                template(v-slot:default='props')
                  v-row
                    v-col(v-for='item in props.items' :key="(item.dish.id, item.mensa.name)" cols='12' sm='6' md='6' lg='4')
                      v-card(height="100%")
                        //- v-img(:alt="item.dish.name" height='250'
                        //-   :src="require('@/assets/quiz_dishes/dish_preview.png')")
                        v-card-title.subheading(style="word-break: normal")
                          | {{ item.dish.name }}
                        v-divider
                        v-col.align-center.justify-center.d-flex.justify-space-between.py-0
                            h4.ma-0.text-right.subheading(:class="{'red--text': $store.state.card_balance <= (parseFloat(item.priceStudent)+1) }")
                                //- (:class="{ 'primary--text': sortBy === key }")
                                | €{{ item.priceStudent }} / €{{ item.priceEmployee }}
                            v-img(v-for="(category, index) in item.dish.categories.length" :alt="item.dish.categories[index].category.name" 
                            height="50" max-width="50" contain :key="index"
                            :src="require('@/assets/dish_icons/food_preferences/'+item.dish.categories[index].category.name+'.png')")
                            v-btn(rounded :href="getGoogleMapsUrl(item.mensa.name)" target="_blank" rel="noopener noreferrer")
                                v-icon mdi-navigation-variant-outline
                                | {{ (item.mensa.name).replace('Bistro Katholische Hochschule', 'Bistro Katho.') }}
                        v-col.align-center.justify-center.d-flex.justify-space-between
                            div
                                span
                                    //- (:class="{ 'primary--text': sortBy === key }")
                                    v-icon mdi-food-apple
                                    | Type: {{ item.dish.main ? 'Main Dish' : 'Supplement' }}
                            div 
                                v-icon mdi-shield-plus-outline
                                span Additives:
                                    //- (:class="{ 'primary--text': sortBy === key }")
                                    span(v-if="item.dish.additives.length == 0")  None
                                    span(v-for="additive in item.dish.additives" :key="additive")  {{ additive.additive.name }}
                        //- Review & Comment Section
                        //- v-col.d-flex.justify-space-between.py-0
                        //-     v-rating(hover length="5" background-color="gray" 
                        //-         v-model="suggested_dish_rating")
                        //-     v-btn(@click="") 
                        //-         v-icon mdi-comment-outline
                        //-         | comment 
                template(v-slot:footer)
                  v-row.mt-2(align='center' justify='center')
                    span.grey--text Items per page
                    v-menu(offset-y)
                      template(v-slot:activator='{ on, attrs }')
                        v-btn.ml-2(dark text color='primary' v-bind='attrs' v-on='on')
                          | {{ itemsPerPage }}
                          v-icon mdi-chevron-down
                      v-list
                        v-list-item(v-for='(number, index) in itemsPerPageArray' :key='index' 
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
            itemsPerPageArray: [4, 8, 12],
            search: "",
            filter: {},
            sortDesc: false,
            page: 1,
            itemsPerPage: 4,
            sortBy: "",
            // TODO: filters:
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
        items () { return this.$store.state.dishplan },
        loaded(){
          // if (typeof this.items !== 'undefined') return true
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
        ...mapActions(["GetDishplan", "GetBalance"]),
    
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
        async getBalance() {
          try {
            await this.GetBalance();
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
        this.getDishplan()
      }
    };
    </script>
    