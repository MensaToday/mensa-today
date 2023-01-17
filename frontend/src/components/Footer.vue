<template lang="pug">
v-footer(dark padless)
    v-row 
        v-col.pb-0.pt-0
            v-card.secondary.text-center(tile)
                v-card-title.center-items
                    div.mt-3
                        v-btn.mx-12.white--text(plain v-for='icon in icons' :key='icon.mdi' icon target="_blank" :href="icon.link")
                            div
                                v-icon(size='24px' elevation='15')
                                    | {{ icon.mdi }}
                                p.mt-2 {{ icon.text }}
                v-divider
                v-card-text.white--text.text-center
                    | {{ new Date().getFullYear() }} &mdash; 
                    strong Marten Jostmann, Leo Giesen, Erik Zimmermann, Marcel Reckmann, Polina Kireyeu
</template>
    
<script>
export default {
    name: "AppFooter",
    data: () => ({
        icons: [
            {
                mdi: "mdi-email",
                link: "mailto:mensa.today@gmail.com",
                text: "Contact",
            },
            {
                mdi: "mdi-github",
                link: "https://github.com/erikzimmermann/data-integration-recommender",
                text: "Code",
            },
            {
                mdi: "mdi-shield-lock",
                link: "/privacy-policy",
                text: "Privacy Policy",
            },
        ],
    })
};
</script>