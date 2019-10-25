<template>
    <v-container>
        This is device detail page. ID: {{ $route.params.id }}
    <data-grid :device="$route.params.id"></data-grid>
    </v-container>
</template>
<script>
import DataGrid from './DataGrid.vue'
export default {
    components: {"data-grid": DataGrid}
}
</script>