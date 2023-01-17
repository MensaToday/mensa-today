<template lang="pug">
v-card.mx-auto.mt-12(max-width='400')
  v-card-title(style="color:grey;") Login
  v-card-text
    v-form(@submit.prevent="submit")
      v-text-field(
        label="ZIV Identifier"
        v-model="form.email")
      v-text-field(
        v-model="form.password"
        label="Password" 
        :type="showPassword ? 'text' : 'password'"
        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" 
        @click:append="showPassword = !showPassword"
        v-on:keyup.enter="login()")
    p(v-if="showError") Identifier or password is incorrect
  v-card-actions
    v-btn(width="100%" dark color="primary" @click="login()") 
      | Login 
  v-card-actions 
    label(style="color:grey;") Not registered yet?
    router-link(to="/quiz" style="color: red;")
      label.ml-1
        a Sign up!
</template>

<script>
import config from "@/config.js";
import JSEncrypt from "jsencrypt";
import { mapActions } from "vuex";
export default {
  name: "LoginUser",
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
      if (process.env.VUE_APP_PRIVATE_KEY) {
        let encryptor = new JSEncrypt();
        encryptor.setPublicKey(this.publicKey);
        return encryptor.encrypt(m);
      } else {
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
