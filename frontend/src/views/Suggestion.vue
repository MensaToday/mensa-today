<template lang="pug">
    div  
        v-container.center-items
            h1.my-4.text-center Your Suggestion Today
            div
                v-divider
                //- Dish Data
                SingleDish(:dishPlan="dishes[0]")
                v-divider 
            div 
                h1.my-4.text-center Other Options
                SingleDish(v-for="(dish, index) in dishes" :key="index" :dishPlan="dish")
            v-btn.px-12(to="/")
                v-icon mdi-chevron-left
                | go home
</template>

<script>
import SingleDish from "@/components/SingleDish.vue";

const sampleDishPlan = {
  dish: {
    id: 154,
    categories: [
      {
        category: {
          id: 1,
          name: "Vegan",
        },
      },
    ],
    main: false,
    name: "Kroketten",
  },
  mensa: {
    id: 9,
    name: "Mensa am Aasee",
    city: "Münster",
    street: "Bismarckallee",
    houseNumber: "11",
    zipCode: 48151,
    startTime: "11:45:00",
    endTime: "14:30:00",
  },
  date: "2022-11-24",
  priceStudent: "0.75",
  priceEmployee: "0.50",
};

export default {
  name: "Suggestion",
  components: {
    SingleDish,
  },
  data() {
    return {
      dishes: [sampleDishPlan, sampleDishPlan, sampleDishPlan],
    };
  }
};
</script>
