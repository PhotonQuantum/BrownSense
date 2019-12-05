<template>
    <v-container>
        <p>This is about page.</p>
    </v-container>
</template>
<script>
    export default {
        created() {
            this.$store.commit("set_nav", [{text: "About", disabled: true}]);
        }
    }
</script>
