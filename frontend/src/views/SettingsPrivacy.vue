<template lang="pug">
v-container(fluid)
  v-alert(dismissible transition="fade-transition" v-if="failed == true" :value="alert" type="error") {{ delete_error_message }}
  div.center-items
    v-row 
      v-col
        SettingsNavigation

        v-card.mx-auto.pa-3
          h2.my-3 Delete Account
          p.mb-3 Once you delete your account, there is no going back. Please be certain.
          v-dialog(
            v-model='deleteAccountDialog' 
            width='30vw')
            template(
              v-slot:activator='{ on, attrs }')
              v-btn(
                color="error"
                @click="deleteAccountDialog"
                v-bind="attrs"
                v-on="on") 
                v-icon mdi-account-remove
                | Delete your account
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
import axios from "axios";
import { mapActions } from "vuex";
import SettingsNavigation from "../components/SettingsNavigation.vue";
export default {
  name: "SettingsPrivacy",
  components: {
    SettingsNavigation
  },
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
    alert(new_val) {
      if (new_val) {
        setTimeout(() => { this.alert = false }, 3000);
      }
    }
  },
  methods: {
    ...mapActions([
      'Logout'
    ]),
    reloadPage() {
      window.location.reload();
    },
    print(msg) {
      console.log(msg)
    },
    async deleteAccount(message) {
      if (message == 'DELETE') {
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

