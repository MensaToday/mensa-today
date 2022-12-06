<template lang="pug">
div  
  v-container
    h1.text-center.my-6 Your Mensa Week
    v-row 
      v-col
        v-data-iterator(:items='items' :items-per-page.sync='itemsPerPage' :page.sync='page' 
          :search='search' :sort-by='sortBy.toLowerCase()' hide-default-footer)
          template(v-slot:header)
            v-toolbar.mb-1(color='primary' dark)
              h3 Recommendations for Today: {{ $store.state.dishplan[0].date }} 
              //- v-spacer
              //- v-text-field(v-model='search' clearable flat solo-inverted hide-details 
              //-   prepend-inner-icon='mdi-magnify' label='Search')
              //- template(v-if='$vuetify.breakpoint.mdAndUp')
              //-   v-spacer
              //-   v-select(v-model='sortBy' flat solo-inverted hide-details :items='keys' 
              //-     prepend-inner-icon='mdi-filter-variant' label='Filter')
          template(v-slot:default='props')
            v-row
              v-col(v-for='item in props.items' :key="(item.dish.id, item.mensa.name)" cols='12' sm='6' md='4' lg='3')
                v-card
                  //- v-img(:alt="item.dish.name" height='250'
                  //-   :src="require('@/assets/quiz_dishes/dish_preview.png')")
                  v-card-title.subheading.font-weight-bold(style="word-break: normal")
                    | {{ item.dish.name }}
                  v-divider
                  v-list(dense)
                    v-list-item
                      v-icon mdi-food
                      v-list-item-content
                        //- (:class="{ 'primary--text': sortBy === key }")
                        | Category
                      v-list-item-content.align-end
                        span(v-for="(key, index) in item.dish.categories.length" :key="index")
                          //- (:class="{ 'primary--text': sortBy === key }" 
                          | {{ item.dish.categories[index].category.name }}
                    v-list-item
                      v-icon mdi-map-marker
                      v-list-item-content
                        //- (:class="{ 'primary--text': sortBy === key }")
                        | Mensa
                      v-list-item-content.align-end
                        //- (:class="{ 'primary--text': sortBy === key }")
                        a(:href="getGoogleMapsUrl(item.mensa.name)" target="_blank" rel="noopener noreferrer")
                          | {{ item.mensa.name }}
                    v-list-item
                      v-icon mdi-cash
                      v-list-item-content
                        //- (:class="{ 'primary--text': sortBy === key }")
                        | Price
                      v-list-item-content.align-end(
                        :class="{ 'red--text': $store.state.card_balance <= (parseFloat(item.priceStudent)+1) }")
                        //- make the item price red, if the card balance does not cover the dish
                        //- (:class="{ 'primary--text': sortBy === key }")
                        | €{{ item.priceStudent }}
                    v-list-item
                      v-icon mdi-food-apple
                      v-list-item-content
                        //- (:class="{ 'primary--text': sortBy === key }")
                        | Type
                      v-list-item-content.align-end
                        //- (:class="{ 'primary--text': sortBy === key }")
                        | {{ item.dish.main ? 'Main Dish' : 'Supplement' }}
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
          //- vuetify v-data-iterator
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "Home",
  data() {
    return {
      items: this.$store.state.dishplan,
      itemsPerPageArray: [4, 8, 12],
      search: "",
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 5,
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
  // created() {
  //   setTimeout(() => {
  //     this.getDishplan()
  //     // this.getBalance()
  //   }, 1000);
  // },
};
</script>
