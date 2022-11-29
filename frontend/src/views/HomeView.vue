<template lang="pug">
div  
  v-container
    v-row
      v-col
        h1.my-4.center-text MensaToday
    v-row.center-items
      v-col
        v-btn(to="/suggestion") Daily Suggesion
        v-btn.ml-10(to="/quiz") Introduction Quiz
    v-row 
      v-col
        h1.center-text Your Mensa Week
    v-row 
      v-col
      v-data-iterator(:items='items' :items-per-page.sync='itemsPerPage' :page.sync='page' :search='search' :sort-by='sortBy.toLowerCase()' :sort-desc='sortDesc' hide-default-footer)
        template(v-slot:header)
          v-toolbar.mb-1(dark color='blue darken-3')
            v-text-field(v-model='search' clearable flat solo-inverted hide-details prepend-inner-icon='mdi-magnify' label='Search')
            template(v-if='$vuetify.breakpoint.mdAndUp')
              v-spacer
              v-select(v-model='sortBy' flat solo-inverted hide-details :items='keys' prepend-inner-icon='mdi-magnify' label='Sort by')
              v-spacer
              v-btn-toggle(v-model='sortDesc' mandatory)
                v-btn(large depressed color='blue' :value='false')
                  v-icon mdi-arrow-up
                v-btn(large depressed color='blue' :value='true')
                  v-icon mdi-arrow-down
        template(v-slot:default='props')
          v-row
            v-col(v-for='item in props.items' :key='item.name' cols='12' sm='6' md='4' lg='3')
              v-card
                v-card-title.subheading.font-weight-bold
                  | {{ item.name }}
                v-divider
                v-list(dense)
                  v-list-item(v-for='(key, index) in filteredKeys' :key='index')
                    v-list-item-content(:class="{ 'blue--text': sortBy === key }")
                      | {{ key }}:
                    v-list-item-content.align-end(:class="{ 'blue--text': sortBy === key }")
                      | {{ item[key.toLowerCase()] }}
        template(v-slot:footer)
          v-row.mt-2(align='center' justify='center')
            span.grey--text Items per page
            v-menu(offset-y)
              template(v-slot:activator='{ on, attrs }')
                v-btn.ml-2(dark text color='primary' v-bind='attrs' v-on='on')
                  | {{ itemsPerPage }}
                  v-icon mdi-chevron-down
              v-list
                v-list-item(v-for='(number, index) in itemsPerPageArray' :key='index' @click='updateItemsPerPage(number)')
                  v-list-item-title {{ number }}
            v-spacer
            span.mr-4.grey--text
              | Page {{ page }} of {{ numberOfPages }}
            v-btn.mr-1(fab dark color='blue darken-3' @click='formerPage')
              v-icon mdi-chevron-left
            v-btn.ml-1(fab dark color='blue darken-3' @click='nextPage')
              v-icon mdi-chevron-right

      //- v-col.cols-4(v-for="idx in 3" :key="idx")
      //-   SingleDish
        //- use slider
        
          //- info button with ingredients
          //- browse section for all dishes on all days 
          //- -> filter out for day, location, food preference, allergies
          //- sort by rating
          //- vuetify v-data-iterator
</template>

<script>
import SingleDish from "@/components/SingleDish.vue";
export default {
  name: "Home",
  components: {
      SingleDish
  },
  data () {
    return {
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 4,
      sortBy: 'name',
      keys: [
        'Name',
        'Calories',
        'Fat',
        'Carbs',
        'Protein',
        'Sodium',
        'Calcium',
        'Iron',
      ],
      items: [
        {
          name: 'Frozen Yogurt',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          sodium: 87,
          calcium: '14%',
          iron: '1%',
        },
        {
          name: 'Ice cream sandwich',
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3,
          sodium: 129,
          calcium: '8%',
          iron: '1%',
        },
        {
          name: 'Eclair',
          calories: 262,
          fat: 16.0,
          carbs: 23,
          protein: 6.0,
          sodium: 337,
          calcium: '6%',
          iron: '7%',
        },
        {
          name: 'Cupcake',
          calories: 305,
          fat: 3.7,
          carbs: 67,
          protein: 4.3,
          sodium: 413,
          calcium: '3%',
          iron: '8%',
        },
        {
          name: 'Gingerbread',
          calories: 356,
          fat: 16.0,
          carbs: 49,
          protein: 3.9,
          sodium: 327,
          calcium: '7%',
          iron: '16%',
        },
        {
          name: 'Jelly bean',
          calories: 375,
          fat: 0.0,
          carbs: 94,
          protein: 0.0,
          sodium: 50,
          calcium: '0%',
          iron: '0%',
        },
        {
          name: 'Lollipop',
          calories: 392,
          fat: 0.2,
          carbs: 98,
          protein: 0,
          sodium: 38,
          calcium: '0%',
          iron: '2%',
        },
        {
          name: 'Honeycomb',
          calories: 408,
          fat: 3.2,
          carbs: 87,
          protein: 6.5,
          sodium: 562,
          calcium: '0%',
          iron: '45%',
        },
        {
          name: 'Donut',
          calories: 452,
          fat: 25.0,
          carbs: 51,
          protein: 4.9,
          sodium: 326,
          calcium: '2%',
          iron: '22%',
        },
        {
          name: 'KitKat',
          calories: 518,
          fat: 26.0,
          carbs: 65,
          protein: 7,
          sodium: 54,
          calcium: '12%',
          iron: '6%',
        },
      ],
    }
  },
  computed: {
    numberOfPages () {
      return Math.ceil(this.items.length / this.itemsPerPage)
    },
    filteredKeys () {
      return this.keys.filter(key => key !== 'Name')
    },
  },
  methods: {
    nextPage () {
      if (this.page + 1 <= this.numberOfPages) this.page += 1
    },
    formerPage () {
      if (this.page - 1 >= 1) this.page -= 1
    },
    updateItemsPerPage (number) {
      this.itemsPerPage = number
    },
  },
};
</script>