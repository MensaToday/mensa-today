<template lang="pug">
v-card.ma-1(light :width="dynamic_card_width")
    v-img(v-show="dish.dish.url != null" :alt="dish.dish.name" :height="img_height" :width="dynamic_card_width" cover :src="dish.dish.url")
    v-card.center-items.light-green.lighten-2.rounded-b-0(v-show="dish.dish.url == null" :height="img_height" elevation="0")
        h1.text--secondary {{ dish.dish.name[0] }}
    v-card-title(style="line-height:1.2; font-size: 17px; word-break: normal; overflow: hidden; white-space: pre-line;")
        | {{ dish.dish.name }}
    v-divider
    v-container.mt-2
        v-row
            v-col.align-center.justify-center.d-flex.justify-space-between.py-0
                h4.ma-0.text-right.subheading(:class="{'red--text': $store.state.card_balance ? $store.state.card_balance <= (parseFloat(dish.priceStudent)+1) : false }")
                    | €{{ dish.priceStudent.replace('.',',') }}/{{ dish.priceEmployee.replace('.',',') }}
                div.d-flex
                    v-img(v-for="(category, index) in dish.dish.categories.length" :alt="dish.dish.categories[index].category.name" 
                        height="50" max-width="50" contain :key="category"
                        :src="require('@/assets/dish_icons/food_preferences/'+dish.dish.categories[index].category.name+'.png')")
        v-row
            v-col.align-center.justify-center.d-flex.justify-space-between
                //- currently redundant information if it is a side dish
                //- span
                //-     v-icon.mr-2 mdi-food-apple
                //-     | {{ dish.dish.main ? 'Main Dish' : 'Side Dish' }}
                div 
                    v-icon.mr-2 mdi-shield-plus-outline
                    span
                        span(v-if="dish.dish.additives.length == 0") None
                        span(v-else v-for="additive in dish.dish.additives" :key="additive.additive.name") 
                            span {{ additive.additive.name }}
                            span(v-show="additive != dish.dish.additives[dish.dish.additives.length-1]") , 
        v-row 
            v-col.align-center.justify-center.d-flex.justify-space-between(v-if="!side_dish")
                div
                    v-icon.mr-2 mdi-thumbs-up-down-outline
                    span(v-if="dish.ext_ratings.rating_count != 0") {{ dish.ext_ratings.rating_avg }}
                    span(v-else) No ratings
                v-rating(hover length="5" background-color="gray" readonly size="24" half-increments)
</template>

<script>
/* eslint-disable */
export default {
    name: "DishCard",
    props: {
        dish: {
            type: Object,
            required: true
        },
        side_dish: {
            type: Boolean,
            default: false
        },
        card_width: {
            type: String,
            default: "20vw"
        },
    },
    data: () => ({
        img_height: "150"
    }),
    methods: {
        getGoogleMapsUrl(mensaName) {
            const url = new URL("https://www.google.com/maps/dir/?api=1");
            url.searchParams.set("destination", mensaName);
            return url.toString();
        },
    },
    computed: {
        // make card width mobile-friendly
        dynamic_card_width() { return this.$vuetify.breakpoint.mdAndUp ? this.card_width : "80vw" }
    }
};
</script>
