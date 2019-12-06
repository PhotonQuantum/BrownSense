<template>
    <doughnut-chart :chart-data="datacollection" :options="chart_options"/>
</template>
<script>
import DoughnutChart from './DoughnutChart.js';
export default {
    data: ()=>({
        chart_options:{cutoutPercentage: 70}
    }),
    props:["online", "offline", "lost"],
    components:{DoughnutChart},
    computed: {
    datacollection: function() {
        return {
            datasets: [{
                data: [this.online, this.offline, this.lost],
                backgroundColor: ["#36a2eb", "#ffcc56", "#fe6383"]
            }],
            labels: [
                'online',
                'offline',
                'lost'
            ]
        }
    },
}
}
</script>