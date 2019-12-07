<template>
    <v-container>
		<v-alert type="error" class="mx-2">
			Page not found.
		</v-alert>
	</v-container>
</template>

<script>
    export default {
        name: "NotFound",
		created() {
            this.$store.commit("set_nav", [{text: "404", disabled: true}]);
        }
    }
</script>

<style scoped>

</style>