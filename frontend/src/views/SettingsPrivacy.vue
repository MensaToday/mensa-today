<template lang="pug">
v-container(fluid)
  v-alert(dismissible transition="fade-transition" v-if="failed == true" :value="alert" type="error") {{ delete_error_message }}
  div.center-items
    v-row 
      v-col(cols="2")
        v-card.mx-auto.my-7(width='300' outlined color="transparent")
          v-list(style="background:transparent;" )
            v-list-item-content
              v-btn.elevation-0(:to='{ name: "SettingsGeneral" }') General
              v-btn.elevation-0(:to='{ name: "SettingsPrivacy" }') Privacy 
      v-col(cols="9")
        v-card.mx-auto.my-12(width='800')
          v-list(style="background:transparent;")
            v-list-item 
              v-list-item-content
                v-list-item-title Delete Account
                  v-list-item-subtitle.mb-3 Once you delete your account, there is no going back. Please be certain.
                  v-dialog(
                    v-model='deleteAccountDialog' 
                    width='30vw')
                    template(
                      v-slot:activator='{ on, attrs }')
                      v-btn(
                        color="error"
                        @click="deleteAccountDialog"
                        v-bind="attrs"
                        v-on="on") Delete your account
                    v-card.py-6
                      v-card-text
                        v-text-field(
                          outlined
                          dense
                          v-model='deleteAccountConfirmation'
                          label='Enter "DELETE" and press Confirm to delete your account.')
                        v-row.ml-1
                          v-btn(
                            @click="deleteAccountDialog = false"
                          ) Cancel 
                          v-btn.ml-2(
                            color="primary"
                            @click="deleteAccount(deleteAccountConfirmation);"
                          ) Confirm

  
</template>

<script>
import { mapActions } from "vuex";
import axios from "axios";
export default {
name: "SettingsPrivacy",
data: () => ({
    deleteAccountDialog: false,
    deleteAccountDialog: false,
    deleteAccountConfirmation: null,

    updatedInfo: {
      mensa_card_id: ""
    },
    failed: false,
    alert: false,
    delete_error_message: "Deleting profile failed!",

}),
watch: {
  alert(new_val){
    if(new_val){
      setTimeout(()=>{this.alert=false}, 3000);
    }
  }
},
methods:{
  ...mapActions([
    'Logout'
  ]),
  reloadPage(){
    window.location.reload();
  },
  print(msg){console.log(msg)
  },
  async deleteAccount(message) {
    if(message == 'DELETE') {
      try {
        await axios.post('user/delete')
        this.logout();
        this.$router.push('/login')

      } catch (error) {
        console.error(error.message)
      }
    }
    else {
      this.failed = true;
      this.alert = true;
      console.error("Wrong delete message!")
    }
  },
  async logout() {
    try {
      await this.Logout();
    } catch (error) {
      console.error(error.message)
    }    
  },
},
computed: {
},
mounted() {
},
created() {
},
};
</script>

