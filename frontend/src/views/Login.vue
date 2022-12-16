<template lang="pug">
div
  v-card.mx-auto.mt-12(max-width='400')
    v-overlay(:absolute="absolute" :value="overlay")
      v-progress-circular(indeterminate color="primary")
    v-img(src="https://www.stw-muenster.de/content/uploads/2016/10/b_DSC0088-1024x680.jpg" height="150px"
      gradient="to bottom right, rgba(135, 135, 135,.5), rgba(135, 135, 135,.5)")
      v-card-title.white--text.justify-center
        h2.my-11 Login
    v-divider
    v-card-text
      v-form(@submit.prevent="submit")
        v-text-field(
          label="ZIV Identifier"
          prepend-icon="mdi-account"
          v-model="form.email")
        v-text-field(
          prepend-icon="mdi-lock" 
          v-model="form.password"
          label="Password" 
          :type="showPassword ? 'text' : 'password'"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" 
          @click:append="showPassword = !showPassword"
          v-on:keyup.enter="login()")
        v-divider
      p(v-if="showError") Identifier or password is incorrect
    
    v-card-actions
        v-btn(@click="$router.push('/quiz')" color="primary") 
            v-icon mdi-account-plus
            | Register
        v-spacer
        v-btn(dark color="green darken-2" @click="login()") 
            v-icon mdi-login-variant
            | Login 
</template>

<script>
import config from "@/config.js";
import JSEncrypt from "jsencrypt";
import { mapActions } from "vuex";
export default {
  name: "Login",
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      showError: false,
      showPassword: false,
      absolute: true,
      overlay: false,
      publicKey: config.publicKey,
    };
  },
  methods: {
    ...mapActions(["Login"]),
    encrypt(m) {
      if(process.env.VUE_APP_PRIVATE_KEY){
        let encryptor = new JSEncrypt();
        encryptor.setPublicKey(this.publicKey);
        return encryptor.encrypt(m);
      } else{
        return m;
      }
    },
    async login() {
      try {
        let User = {
          username: this.form.email,
          password: this.encrypt(this.form.password),
        };
        await this.Login(User);
        // reset form
        this.form = { email: "", password: "" };
        this.overlay = true;
        this.showError = false;
        this.$router.push("/");
      } catch (error) {
        console.log(error);
        this.showError = true;
      }
    },
  },
};
</script>
