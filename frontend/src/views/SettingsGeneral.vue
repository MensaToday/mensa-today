<template lang="pug">
v-container(fluid)
  v-alert(dismissible transition="fade-transition" v-if="failed == false" :value="alert" type="success") {{ update_success_message }}
  v-alert(dismissible transition="fade-transition" v-if="failed == true" :value="alert" type="error") {{ update_error_message }}

  div.center-items
    v-row
      v-col
        SettingsNavigation

        v-card.mx-auto
          v-list(style="background:transparent;")
            v-list-item 
              v-list-item-content
                v-list-item-title Username
                v-text-field(disabled :value="user_data.username")
            v-list-item 
              v-list-item-content 
                v-list-item-title Mensa Card ID
                v-text-field(v-model="updatedInfo.mensa_card_id" ) 
            v-list-item 
              v-list-item-content 
                //- Food Preference pane
                v-list-item-title Food Preferences 
                v-card.elevation-0
                  v-card-text
                    v-row
                    v-row
                      v-col.py-0(cols="4" v-for="(value, food_preference, index) in food_preferences" :key="index")
                        v-checkbox.mx-3(
                          v-model="food_preferences[food_preference]"
                          :label="food_preference")
                      v-col.py-0(cols="4")
                        v-checkbox.mx-3(
                          @click="isCheckAll ? uncheckAll() : checkAll()"
                          v-model="isCheckAll"
                          label="Select All")
                    v-row
                      v-col(cols="6")
                        v-combobox(v-model='selected_allergies' :items='Object.keys(allergies)' 
                          :search-input.sync='search' hide-selected label='Specify Allergies' 
                          multiple persistent-hint small-chips clearable)
                          template(v-slot:no-data)
                            v-list-item
                              v-list-item-content
                                v-list-item-title
                                  | No results matching &quot;
                                  strong {{ search }}
                                  | &quot;. 
                      v-col(cols="6")
                        v-combobox(v-model='selected_additives' :items='Object.keys(additives)' 
                          :search-input.sync='search' hide-selected 
                          label='Specify Additives You Dislike' 
                          multiple persistent-hint small-chips clearable)
                          template(v-slot:no-data)
                            v-list-item
                              v-list-item-content
                                v-list-item-title
                                  | No results matching &quot;
                                  strong {{ search }}
                                  | &quot;.

            v-list-item.justify-end
              v-btn(color="primary" 
                @click="updateObject(allergies, selected_allergies); updateObject(additives, selected_additives); updateSelectedCategories(); updateUserInfo(updatedInfo.mensa_card_id, selected_categories, selected_allergies);") 
                v-icon mdi-account-check
                | Update Profile

</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";
import SettingsNavigation from "../components/SettingsNavigation.vue";
export default {
  name: "SettingsGeneral",
  components: {
    SettingsNavigation
  },
  data: () => ({

    updatedInfo: {
      mensa_card_id: ""
    },
    failed: false,
    alert: false,
    update_error_message: "Updating profile failed!",
    update_success_message: "Profile updated successfully!",

    food_preferences: {
      Vegan: false,
      Vegetarian: false,
      Pork: false,
      Beef: false,
      Poultry: false,
      Alcohol: false,
      Fish: false,
    },
    additives: {
      Dyed: false,
      Preservatives: false,
      Antioxidants: false,
      "Flavor enhancers": false,
      Sulphurated: false,
      Blackened: false,
      Waxed: false,
      Phosphate: false,
      Sweeteners: false,
      "Phenylalanine source": false,
    },
    allergies: {
      Gluten: false,
      Spelt: false,
      Barles: false,
      Oats: false,
      Kamut: false,
      Rye: false,
      Wheat: false,
      Crustaceans: false,
      Egg: false,
      Fish: false,
      Peanuts: false,
      Soy: false,
      Milk: false,
      Nuts: false,
      Almonds: false,
      Hazelnuts: false,
      Walnuts: false,
      Cashews: false,
      Pecans: false,
      "Brazil nuts": false,
      Pistachios: false,
      Macadamias: false,
      Celerey: false,
      Mustard: false,
      Sesame: false,
      Lupines: false,
      Molluscs: false,
      "Sulfur dioxide": false,
    },
    search: null,
    selected_categories: [],
    selected_allergies: [],
    selected_additives: [],

  }),
  watch: {
    alert(new_val) {
      if (new_val) {
        setTimeout(() => { this.alert = false }, 3000);
      }
    }
  },
  methods: {
    ...mapActions([
      'GetUserData',
      'GetBalance'
    ]),
    reloadPage() {
      window.location.reload();
    },
    updateSelectedCategories() {
      this.selected_categories = [];
      for (const [key, value] of Object.entries(this.food_preferences)) {
        if (value) {
          this.selected_categories.push(key);
        }
      }
    },
    setPreferenceData() {

      for (const [a, b] of Object.entries(this.$store.state.user.food_categories)) {
        this.food_preferences[b.category.name] = true;
      }
      for (const [a, b] of Object.entries(this.$store.state.user.food_allergies)) {
        this.allergies[b.allergy.name] = true;
        this.selected_allergies.push(b.allergy.name);
        this.updateObject(this.allergies, b.allergy.name);
      }
      this.updateSelectedCategories();

    },
    updateObject(obj, values) {
      for (let idx = 0; idx < values.length; idx++) {
        obj[values[idx]] = true;
      }
    },
    print(msg) { console.log(msg) },
    async getUserData() {
      try {
        await this.GetUserData();
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
    async deleteAccount(message) {
      if (message == 'DELETE') {
        try {
          await axios.post('user/delete')
        } catch (error) {
          console.error(error.message)
        }
      }
      else { console.error("Wrong delete message!") }
    },
    async updateUserInfo(card_id, categories, allergies) {
      if (card_id != null) {
        try {
          //Update Mensa Card ID
          await axios.post('user/update_card_id', {
            card_id: card_id
          });

          //Update Categories and Allergies
          await axios.post('user/update_preferences', {
            categories: categories,
            allergies: allergies
          });

          this.failed = false;
          this.alert = true;
          this.getBalance();

        } catch (error) {
          console.error(error.message)
          this.failed = true;
          this.alert = true;
        }

      }
      this.selected_categories = [];
      this.selected_allergies = [];
      this.getUserData();
    },
    checkAll() {
      Object.keys(this.food_preferences).forEach((key) => {
        this.food_preferences[key] = true;
      });
    },
    uncheckAll() {
      Object.keys(this.food_preferences).forEach((key) => {
        this.food_preferences[key] = false;
      });
    },
  },
  computed: {
    isCheckAll: {
      get: function () {
        for (let [, value] of Object.entries(this.food_preferences)) {
          if (value == false) return false;
        }
        return true;
      },
      set: function () {
        return false;
      },
    },
    user_data() { return this.$store.state.user; },
  },
  mounted() {
    //this.getUserData();
  },
  created() {
    this.setPreferenceData();
    this.updatedInfo.mensa_card_id = this.user_data.mensa_card_id;
  },
};
</script>

