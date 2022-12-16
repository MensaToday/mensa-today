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
                            v-img(v-if="this.$store.state.user.avatar"
                                :src="$store.state.user.avatar" alt="User Profile")
                            v-card.center-items.primary.rounded-b-0(
                                v-else height='250' width='250')
                                h1(v-if="this.$store.state.user.first_name && this.$store.state.user.last_name") 
                                    | {{ this.$store.state.user.first_name[0] }}{{ this.$store.state.user.last_name[0] }}
                    v-col(cols='8')
                        h2.my-3(v-if="this.$store.state.user.first_name && this.$store.state.user.last_name") 
                            | {{ this.$store.state.user.first_name + " " + this.$store.state.user.last_name}}
                        v-list(style="background: transparent;")
                            v-list-item
                                v-list-item-icon
                                    v-icon(color='white') mdi-card-account-details
                                v-list-item-content.white--text {{ this.$store.state.user.mensa_card_id }}
                            v-list-item
                                v-list-item-icon
                                    v-icon(color='white') mdi-email
                                v-list-item-content.white--text {{ this.$store.state.user.email }}@uni-muenster.de
                      
            
        //- Start Profile Data
        //- v-card-actions.justify-center
          v-dialog(
            persistent
            v-model='changeUserInfoDialog' 
            width='60vw')
            template(
              v-slot:activator='{ on, attrs }')
              v-btn(
                color="primary"
                @click="setFormDataUpdate(); changeUserInfoDialog"
                v-bind="attrs"
                v-on="on") Edit
            v-card.py-3
              v-card-text
                v-row
                  v-col
                    v-text-field(
                      outlined
                      dense
                      v-model='updatedU.fname'
                      prepend-icon='mdi-account'
                      label='First Name')
                  v-col
                    v-text-field(
                      outlined
                      dense
                      v-model='updatedU.lname'
                      label='Last Name')
                v-text-field(
                  outlined
                  dense
                  v-model='updatedU.email'
                  prepend-icon='mdi-email'
                  label='Email')
                v-row
                  v-col(cols=9)
                    v-file-input(
                      outlined
                      dense
                      :rules="rules"
                      accept="image/png, image/jpeg, image/jpg, image/gif"
                      placeholder="Pick an avatar"
                      prepend-icon="mdi-camera"
                      label="Avatar"
                      @change="onFileSelected"
                    )
                  v-col(cols=3)
                    v-btn(
                      block
                      :disabled="invalidUpload"
                      @click="onUpload(); selectedFile = null"
                    ) Upload
                v-row
                  v-col.text-center(
                    v-for='(picture, index) in defaultPics' 
                    :key='index')
                    v-avatar(
                      size='100')
                      v-img(
                        :src="picture")
                    v-btn.mt-3(
                      @click='use(index)'
                      ) Use
  
            //-   v-card-actions
            //-     v-btn(
            //-       @click='changeUserInfoDialog = false; resetUpdatedU()' color="primary") Close
            //-     v-spacer
            //-     v-btn(
            //-       @click='updateUser(); changeUserInfoDialog = false;' color="primary") Save
            //-   v-alert(type="error" v-if="changeUserInfoDialogError").text-center.mt-5.mb-0 {{ changeUserInfoDialogErrorMessage }}
        //- v-card-actions.justify-center
        //-   v-btn(small text
        //-     @click="$router.push('/password_reset')") Change Password
            
  
        //- End Profile Data
        //- v-expansion-panels(flat, accordion)
          v-expansion-panel
            v-expansion-panel-header(hide-actions)
              v-btn(text color="primary") Set New Password
            v-expansion-panel-content
              v-form(@submit.prevent="submit")
                v-text-field(
                  prepend-icon="mdi-lock"
                  v-model="form.password"
                  label="New Password"
                  :type="showPassword ? 'text' : 'password'"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append="showPassword = !showPassword"
                )
                v-text-field(
                  prepend-icon="mdi-lock"
                  v-model="form.passwordRepeat"
                  label="Repeat Password"
                  :type="showPassword ? 'text' : 'password'"
                )
                p(v-if="showError").error--text.text-center Passwords do not match
                v-card-actions
                  v-spacer
                  v-btn(color="primary" type="submit") Set new Password
                v-alert(:value="isSet" dense outlined text type="success" width="100%") {{ response }}
                
</template>

<script>
export default {
name: "UserProfile",
data: () => ({
    // form:{
    //     password: "",
    //     passwordRepeat: "",
    // },
    // response: "",
    // isSet: false,
    // showPassword: false,
    // showError: false,
    // // Change user info
    // overlay: false,
    // changeUserInfoDialog: false,
    // changeUserInfoDialogError: false,
    // changeUserInfoDialogErrorMessage: "Something went wrong. Please check if your email or matriculation number are not taken",
    // updatedU: {
    // email: null,
    //     fname: null,
    //     lname: null
    // },

    // // Change avatar
    // changeAvatarDialog: false,
    // // custom image 
    // rules: [
    // value => !value || value.size < 1100000 || 'Avatar size should be less than 1.1 MB!',
    // ],
    // selectedFile: null,
}),
computed: {
//   ...mapGetters([
//     'permissionLevelString',
//     'checkIfCustomImage'
//   ]), 
//   ...mapState ({
//     user: state => state.auth.user,
//     avatar: state => state.auth.user.avatar,
//     avatarBase64: state => state.auth.avatarBase64,
//   }),
//   invalidUpload() {
//     if(this.selectedFile != null && this.selectedFile.size < 1100000) return false
//     else return true
//   },
},

methods:{
//   ...mapActions([
//     'UpdateUser', 
//     'GetAvatarBase64',
//     'GetSessionRoleByUserAndSessionId',
//     'NewPassword'
//   ]),
//   async submit(){
//     if(this.form.password != this.form.passwordRepeat){
//       this.showError = true
//     } else {
//       const password = { "password": this.form.password }
//       try{
//           await this.NewPassword([password, this.user.id])
//           let i = this.$store.state.UserManagement.response.indexOf(":")
//           this.response = this.$store.state.UserManagement.response.slice(i+2, this.$store.state.UserManagement.response.length-2)
//           this.isSet = true
//           window.setInterval(()=> {
//             this.isSet = false
//             }, 5000)
//       } catch(error){
//           console.error(error)
//           this.error = true
//         }
//     }
//   },

//   use: function(PictureIndex){
//     this.setDefaultImage(PictureIndex)
//   },
//   resetUpdatedU() {
//     this.updatedU = {
//       email: null,
//       fname: null,
//       lname: null
//     }
//   },
//   onFileSelected(event) {
//     this.selectedFile = event
//   },
//   setFormDataUpdate() {
//     this.updatedU.email = this.user.email,
//     this.updatedU.fname = this.user.first_name,
//     this.updatedU.lname = this.user.last_name
//   },
//   async updateUser() {
//     let user = this.user
//     let updatedU = this.updatedU
//     const User = {
//       "avatar": user.avatar,
//       "email": updatedU.email ? updatedU.email : user.email,
//       "first_name": updatedU.fname ? updatedU.fname : user.first_name,
//       "last_name": updatedU.lname ? updatedU.lname : user.last_name,
//       "id": user.id,
//       "matriculation_number": user.matriculation_number,
//       "permission": user.permission,
//     }
    
//     try {
//       await this.UpdateUser(User);
//       // reset the form
//       this.updatedU = {
//         email: null,
//         fname: null,
//         lname: null
//       }
//       // this.changeUserInfoDialog = false
//     } catch (error) {
//       this.changeUserInfoDialogError = true
//       console.error(error)
//     }
//   },
//   async setDefaultImage(PictureIndex){
//     let user = this.user
//     const User = {
//       "avatar": PictureIndex,
//       "email": user.email,
//       "first_name": user.first_name,
//       "last_name": user.last_name,
//       "id": user.id,
//       "matriculation_number": user.matriculation_number,
//       "permission": user.permission,
//     }
//     try {
//       await this.UpdateUser(User);
//     } catch (error) {
//       console.error(error)
//     }
//   },
//   async onUpload () {
//     let user_id = this.user.id
//     let selectedFile = this.selectedFile
//     const fd = new FormData()
//     fd.append('document', selectedFile, selectedFile.name)
//     try {
//       await axios.post('users/' + user_id + '/avatar', fd)
//       this.$store.dispatch('getAllUserData', user_id)
//     } catch (error) {
//       console.error("error.message")
//       console.error(error.message)
//     }
//   },
//   async getAvatar(){
//     try {
//       await this.GetAvatarBase64()
//     }
//     catch(error) { console.error(error) }
//   },
},

created() {
//   if (this.avatar == null) this.setDefaultImage(0)
//   if(this.checkIfCustomImage) this.getAvatar()
},
};
</script>

