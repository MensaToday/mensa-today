<template lang="pug">
v-container(fluid)
    v-card.mx-auto.my-12(max-width='800' tile)
        v-img(height="256px"
            src="https://www.stw-muenster.de/content/uploads/2016/10/b_DSC0088-1024x680.jpg"
            gradient="to bottom right, rgba(135, 135, 135,.5), rgba(135, 135, 135,.5)") 
            v-card-title.white--text.mt-6
                v-row 
                    v-col(cols='4').center-items
                        v-avatar(size='128')
                            v-card.center-items.primary.rounded-b-0(height="128", width="128")
                              v-icon(size="64",color='white') mdi-account-school
                              
                    v-col(cols='4')
                        v-list(style="background: transparent;")
                            v-list-item
                                v-list-item-icon
                                    v-icon(color='white') mdi-account-box
                                v-list-item-content.white--text {{ this.$store.state.user.username }} 
                            v-list-item
                                v-list-item-icon
                                    v-icon(color='white') mdi-card-bulleted
                                v-list-item-content.white--text(:key="updateElement") {{ this.$store.state.user.mensa_card_id }}
                                  
        //- //- Start Profile Data
        //- v-card-actions.justify-center
        //-   v-dialog(
        //-     v-model='changeUserInfoDialog' 
        //-     width='60vw')
        //-     template(
        //-       v-slot:activator='{ on, attrs }')
        //-       v-btn(
        //-         color="primary"
        //-         @click="setFormDataUpdate(); changeUserInfoDialog"
        //-         v-bind="attrs"
        //-         v-on="on") Edit Personal Information
        //-     v-card.py-3.pt-md-6
        //-       v-card-text
        //-         v-row
        //-           v-col
        //-             v-text-field(
        //-               outlined
        //-               dense
        //-               v-model='updatedU.fname'
        //-               prepend-icon='mdi-account'
        //-               label='First Name')
        //-           v-col
        //-             v-text-field(
        //-               outlined
        //-               dense
        //-               v-model='updatedU.lname'
        //-               label='Last Name')
        //-         v-text-field(
        //-           outlined
        //-           dense
        //-           v-model='updatedU.email'
        //-           prepend-icon='mdi-email'
        //-           label='Email')
        //-         v-text-field(
        //-           outlined
        //-           dense
        //-           v-model='updatedU.card_id'
        //-           prepend-icon='mdi-card-bulleted'
        //-           label='Mensa Card ID')
      
                //- v-row
                //-   v-col(cols=9)
                //-     v-file-input(
                //-       outlined
                //-       dense
                //-       :rules="rules"
                //-       accept="image/png, image/jpeg, image/jpg, image/gif"
                //-       placeholder="Pick an avatar"
                //-       prepend-icon="mdi-camera"
                //-       label="Avatar"
                //-       @change="onFileSelected"
                //-     )
                //-   v-col(cols=3)
                //-     v-btn(
                //-       block
                //-       :disabled="invalidUpload"
                //-       @click="onUpload(); selectedFile = null"
                //-     ) Upload
                //- v-row
                //-   v-col.text-center(
                //-     v-for='(picture, index) in defaultPics' 
                //-     :key='index')
                //-     v-avatar(
                //-       size='100')
                //-       v-img(
                //-         :src="picture")
                //-     v-btn.mt-3(
                //-       @click='use(index)'
                //-       ) Use
              v-card-actions
                v-btn(
                  @click='changeUserInfoDialog = false; resetUpdatedU()' color="primary") Close
                v-spacer
                v-btn(
                  @click='updateUser(); changeUserInfoDialog = false;' color="primary") Save
              v-alert(type="error" v-if="changeUserInfoDialogError").text-center.mt-5.mb-0 {{ changeUserInfoDialogErrorMessage }}

        //- v-card-actions.justify-center
        //-   v-btn(small text
        //-     @click="$router.push('/password_reset')") Change Password
            
  
        //- //End Profile Data
        //- v-expansion-panels(flat, accordion)
        //-   v-expansion-panel
        //-     v-expansion-panel-header(hide-actions)
        //-       v-btn(text color="primary") Set New Password
        //-     v-expansion-panel-content
        //-       v-form(@submit.prevent="submit")
        //-         v-text-field(
        //-           prepend-icon="mdi-lock"
        //-           v-model="form.password"
        //-           label="New Password"
        //-           :type="showPassword ? 'text' : 'password'"
        //-           :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        //-           @click:append="showPassword = !showPassword"
        //-         )
        //-         v-text-field(
        //-           prepend-icon="mdi-lock"
        //-           v-model="form.passwordRepeat"
        //-           label="Repeat Password"
        //-           :type="showPassword ? 'text' : 'password'"
        //-         )
        //-         p(v-if="showError").error--text.text-center Passwords do not match
        //-         v-card-actions
        //-           v-spacer
        //-           v-btn(color="primary" type="submit") Set new Password
        //-         v-alert(:value="isSet" dense outlined text type="success" width="100%") {{ response }}
        v-card-actions.justify-center 
          v-dialog(
            v-model='changeUserInfoDialog' 
            width='60vw')
            template(
              v-slot:activator='{ on, attrs }')
              v-btn(
                color="primary"
                @click="changeUserInfoDialog = true"
                v-bind="attrs"
                v-on="on") Update Account Settings
            v-card.py-3.pt-md-6
              v-card-text
                v-row
                  v-text-field(
                    outlined
                    dense
                    v-model='updatedUserInfo.mensa_card_id'
                    prepend-icon='mdi-card-bulleted'
                    label='Mensa Card ID (7 digits)')    
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
                v-btn.ml-8(
                  color="primary"
                  @click="changeUserInfoDialog = false"
                ) Cancel 
                v-btn.ml-3(
                  color="primary"
                  @click="updateObject(allergies, selected_allergies); updateObject(additives, selected_additives); updateSelectedCategories(); updateUserInfo(updatedUserInfo.mensa_card_id, selected_categories, selected_allergies); changeUserInfoDialog = false"
                ) Save

        v-card-actions.justify-center
          v-dialog(
            v-model='deleteAccountDialog' 
            width='60vw')
            template(
              v-slot:activator='{ on, attrs }')
              v-btn(
                @click="deleteAccountDialog"
                v-bind="attrs"
                v-on="on") Delete Account
            v-card.py-3.pt-md-6
              v-card-text
                v-text-field(
                  outlined
                  dense
                  v-model='deleteAccountConfirmation'
                  label='Enter "DELETE" and press Confirm to delete your account.'
                  prepend-icon='mdi-account')
                v-btn.ml-8(
                  color="primary"
                  @click="deleteAccountDialog = false"
                ) Cancel 
                v-btn.ml-3(
                  color="primary"
                  @click="deleteAccount(deleteAccountConfirmation);"
                ) Confirm
                 

        
                
</template>

<script>
import { mapActions } from "vuex";
import { mapGetters } from "vuex";
import { mapState } from "vuex";
import axios from "axios";
export default {
name: "UserProfile",
data: () => ({
    form:{
        password: "",
        passwordRepeat: "",
    },
    response: "",
    isSet: false,
    showPassword: false,
    showError: false,
    // Change user info
    overlay: false,
    changeUserInfoDialog: false,
    changeUserInfoDialogError: false,
    changeUserInfoDialogErrorMessage: "Something went wrong. Please check if your email or matriculation number are not taken",
    deleteAccountDialog: false,
    deleteAccountConfirmation: null,
    updatedUserInfo: {
      mensa_card_id: null
    },
    updateElement: 0,

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
       
    // Change avatar
    // changeAvatarDialog: false,
    // custom image 
    // rules: [
    // value => !value || value.size < 1100000 || 'Avatar size should be less than 1.1 MB!',
    // ],
    // selectedFile: null,
}),
computed: {
  ...mapGetters([
    'permissionLevelString',
    'checkIfCustomImage'
  ]), 
  ...mapState ({
    user: state => state.auth.user,
    // avatar: state => state.auth.user.avatar,
    // avatarBase64: state => state.auth.avatarBase64,
  }),
  invalidUpload() {
    if(this.selectedFile != null && this.selectedFile.size < 1100000) return false
    else return true
  },
},

methods:{
  ...mapActions([
    // 'UpdateUser', 
    // 'GetAvatarBase64',
    // 'GetSessionRoleByUserAndSessionId',
    // 'NewPassword',
    'GetUserData'
  ]),
  forceRenderer(){
    this.updateElement += 1;
  },
  updateSelectedCategories() {
      // Object.entries(this.food_preferences).forEach((key, value) =>
      for (const [key, value] of Object.entries(this.food_preferences)) {
        if (value) {
          this.selected_categories.push(key);
        }
      }
    },
  updateObject(obj, values) {
    for (let idx = 0; idx < values.length; idx++) {
      obj[values[idx]] = true;
    }
  },
  async getUserData(){
    try {
        await this.GetUserData();
      } catch (error) {
        console.log(error);
    }
  },
  async deleteAccount(message) {
    if(message == 'DELETE') {
      try {
        await axios.post('user/delete')
      } catch (error) {
        console.error(error.message)
      }
    }
    else {console.error("Wrong delete message!")}
  },
  async updateUserInfo(card_id, categories, allergies) {
    console.log(card_id);
    console.log(categories);
    console.log(allergies);
    if(card_id != null) {
    try {
      //Update Mensa Card Id
      await axios.post('user/update_card_id', {
        card_id: card_id
      });
      } catch (error) {
      console.error(error.message)
      }
    }
      await axios.post('user/update_preferences', {
        categories: categories,
        allergies: allergies
      });

    
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
  // async submit(){
  //   if(this.form.password != this.form.passwordRepeat){
  //     this.showError = true
  //   } else {
  //     const password = { "password": this.form.password }
  //     try{
  //         await this.NewPassword([password, this.user.id])
  //         let i = this.$store.state.UserManagement.response.indexOf(":")
  //         this.response = this.$store.state.UserManagement.response.slice(i+2, this.$store.state.UserManagement.response.length-2)
  //         this.isSet = true
  //         window.setInterval(()=> {
  //           this.isSet = false
  //           }, 5000)
  //     } catch(error){
  //         console.error(error)
  //         this.error = true
  //       }
  //   }
  // },

  // use: function(PictureIndex){
  //   this.setDefaultImage(PictureIndex)
  // },
  // resetUpdatedU() {
  //   this.updatedU = {
  //     email: null,
  //     fname: null,
  //     lname: null
  //   }
  // },
  // onFileSelected(event) {
  //   this.selectedFile = event
  // },
  // setFormDataUpdate() {
  //   this.updatedU.email = this.user.email,
  //   this.updatedU.fname = this.user.first_name,
  //   this.updatedU.lname = this.user.last_name
  // },
  // async updateUser() {
  //   let user = this.user
  //   let updatedU = this.updatedU
  //   const User = {
  //     "avatar": user.avatar,
  //     "email": updatedU.email ? updatedU.email : user.email,
  //     "first_name": updatedU.fname ? updatedU.fname : user.first_name,
  //     "last_name": updatedU.lname ? updatedU.lname : user.last_name,
  //     "id": user.id,
  //     "matriculation_number": user.matriculation_number,
  //     "permission": user.permission,
  //   }
    
  //   try {
  //     await this.UpdateUser(User);
  //     // reset the form
  //     this.updatedU = {
  //       email: null,
  //       fname: null,
  //       lname: null
  //     }
  //     this.changeUserInfoDialog = false
  //   } catch (error) {
  //     this.changeUserInfoDialogError = true
  //     console.error(error)
  //   }
  // },
  // async setDefaultImage(PictureIndex){
  //   let user = this.user
  //   const User = {
  //     "avatar": PictureIndex,
  //     "email": user.email,
  //     "first_name": user.first_name,
  //     "last_name": user.last_name,
  //     "id": user.id,
  //     "matriculation_number": user.matriculation_number,
  //     "permission": user.permission,
  //   }
  //   try {
  //     await this.UpdateUser(User);
  //   } catch (error) {
  //     console.error(error)
  //   }
  // },
  // async onUpload () {
  //   let user_id = this.user.id
  //   let selectedFile = this.selectedFile
  //   const fd = new FormData()
  //   fd.append('document', selectedFile, selectedFile.name)
  //   try {
  //     await axios.post('users/' + user_id + '/avatar', fd)
  //     this.$store.dispatch('getAllUserData', user_id)
  //   } catch (error) {
  //     console.error("error.message")
  //     console.error(error.message)
  //   }
  // },
  // async getAvatar(){
  //   try {
  //     await this.GetAvatarBase64()
  //   }
  //   catch(error) { console.error(error) }
  // },
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
},

created() {
  this.getUserData();
  // if (this.avatar == null) this.setDefaultImage(0)
  // if(this.checkIfCustomImage) this.getAvatar()
  console.log(this.$store.state)
},
};
</script>

