<template lang="pug">
div  
  v-container
    h1.text-center.my-6 Your Mensa Week

    v-row 
      v-col
        v-data-iterator(:items='items' :items-per-page.sync='itemsPerPage' :page.sync='page' :search='search' :sort-by='sortBy.toLowerCase()' hide-default-footer)
          template(v-slot:header)
            v-toolbar.mb-1(color='primary' dark)
              v-text-field(v-model='search' clearable flat solo-inverted hide-details prepend-inner-icon='mdi-magnify' label='Search')
              template(v-if='$vuetify.breakpoint.mdAndUp')
                v-spacer
                v-select(v-model='sortBy' flat solo-inverted hide-details :items='keys' prepend-inner-icon='mdi-filter-variant' label='Filter')
          template(v-slot:default='props')
            v-row
              v-col(v-for='item in props.items' :key='item.name' cols='12' sm='6' md='4' lg='3')
                v-card
                  v-card-title.subheading.font-weight-bold
                    | {{ item.name }}
                  v-divider
                  v-list(dense)
                    v-list-item(v-for='(key, index) in filteredKeys' :key='index')
                      v-list-item-content(:class="{ 'primary--text': sortBy === key }")
                        | {{ key }}:
                      v-list-item-content.align-end(:class="{ 'primary--text': sortBy === key }")
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
export default {
  name: "Home",
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
        'Food_Preferences',
        'Allergies',
        'Additives'
      ],
      items: [
        {name: "Dish Name1", food_preferences: "Vegan", allergies: ["Gluten"], additives: ["Dyed"]},
        {name: "Dish Name2", food_preferences: "Vegetarian", allergies: ["Spelt"], additives: ["Preservatives"]},
        {name: "Dish Name3", food_preferences: "Beef", allergies: ["Barles"], additives: ["Antioxidants"]},
        {name: "Dish Name4", food_preferences: "Alcohol", allergies: ["Oats"], additives: ["Sulphurated"]},
        {"name": "Dish Name5", "food_preferences": [], "allergies": [], "additives": []}
      ]
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