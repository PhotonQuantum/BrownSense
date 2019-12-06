<template>
    <doughnut-chart :chart-data="datacollection" :options="chart_options"/>
</template>
<script>
import DoughnutChart from './DoughnutChart.js';
export default {
    data: ()=>({
        chart_options:{cutoutPercentage: 70}
    }),
    props:["working", "pending"],
    components:{DoughnutChart},
    computed: {
    datacollection: function() {
        return {
            datasets: [{
                data: [this.working, this.pending],
                backgroundColor: ["#36a2eb", "#757575"]
            }],
            labels: [
                'working',
                'pending'
            ]
        }
    },
}
}
</script>