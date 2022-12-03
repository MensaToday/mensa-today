<template lang="pug">
v-container
    v-card.mx-auto.mt-12(max-width='400')
        v-overlay(:absolute="absolute" :value="overlay")
            v-progress-circular(indeterminate color="primary")
        v-card-title
            h2.my-3 Login
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
            v-btn(@click="this.$router.push('/quiz')" color="primary") 
                v-icon mdi-account-plus
                | Register
            v-spacer
            v-btn(dark color="green darken-2" @click="login()") 
                v-icon mdi-login-variant
                | Login 
</template>

<script>
import { mapActions } from "vuex";
export default {
    name: "Login",
    data () {
    return {
        form: {
            email: "",
            password: ""
        },
        showError: false,
        showPassword: false,
        absolute: true,
        overlay: false
    }
},
    methods: {
        ...mapActions(["Login"]),   

        async login() {
            try {
                let User = {
                    'username': this.form.email,
                    'password': this.form.password
                }
                await this.Login(User);
                // reset form
                this.form = {email: "", password: ""}
                // wait 3 seconds before navigating to the displan because the api call takes so long
                // it is not a best practice 😵‍💫
                this.overlay = true
                setTimeout(() => { 
                    if(this.$store.state.dishplan){
                        this.showError = false
                        this.$router.push('/')
                    }
                }, 3000);
            } catch (error) {
                console.log(error)
                this.showError = true
            }
        }
    },
};
</script>