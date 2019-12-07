<template>

    <v-row justify="center">
        <v-col cols="12">
            <v-card>
                <v-card-title>
                    <v-list-item two-line>
                        <v-list-item-content class="text-center">
                            <v-list-item-subtitle>Hydrogen Sulfide</v-list-item-subtitle>
                            <v-list-item-title class="headline">{{ this_device.h2s }} PPM
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-card-title>
                <v-card-text>
                    <div class="grey lighten-4 pa-6">
                        <line-chart
                                class="sensor-graph"
                                :chart-data="h2s_collection"
                                :options="chart_options"
                        />
                    </div>
                </v-card-text>
            </v-card>
        </v-col>
        <v-col cols="12">
            <v-card>
                <v-card-title>
                    <v-list-item two-line>
                        <v-list-item-content class="text-center">
                            <v-list-item-subtitle>Ammonia</v-list-item-subtitle>
                            <v-list-item-title class="headline">{{ this_device.nh3 }} PPM
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-card-title>
                <v-card-text>
                    <div class="grey lighten-4 pa-6">
                        <line-chart
                                class="sensor-graph"
                                :chart-data="nh3_collection"
                                :options="chart_options"
                        />
                    </div>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
    import {mapState} from 'vuex';
    import LineChart from "./LineChart.js";
    import VueScreenSize from 'vue-screen-size';

    export default {
        name: "Graph",
        mixins: [VueScreenSize.VueScreenSizeMixin],
        components: {LineChart},
        data: () => ({
            h2s_collection: {},
            nh3_collection: {},
            this_device: {h2s: "N/A", nh3: "N/A"}
        }),
        computed: {
            ...mapState([
                "dbs"
            ]),
            device: function () {
                return this.$route.params.id;
            },
            chart_options: function () {
                return {
                    maintainAspectRatio: false,
                    legend: {
                        display: false
                    },
                    elements: {
                        line: {
                            cubicInterpolationMode: 'monotone'
                        }
                    },
                    animation: {
                        duration: 0 // general animation time
                    },
                    scales: {
                        xAxes: [
                            {
                                type: "time",
                                time: {
                                    parser: "x"
                                },
                                gridLines: {
                                    display: false
                                },
                                display: (this.$vssWidth > 600)
                            }
                        ],
                        yAxes: [{
                            gridLines: {
                                display: false
                            }
                        }]
                    }
                }
            }
        },
        pouch: {
            this_device() {
                return {
                    database: this.dbs["summary"],
                    selector: {
                        device: this.device
                    },
                    first: true
                }
            },
            h2s_grid() {
                return {
                    database: this.dbs["datagrid"],
                    selector: {
                        device: this.device,
                        type: "h2s",
                        time: {$gt: new Date() / 1000 - 1000}
                    },
                    sort: [{time: "desc"}],
                    limit: 200
                }
            },
            nh3_grid() {
                return {
                    database: this.dbs["datagrid"],
                    selector: {
                        device: this.device,
                        type: "nh3",
                        time: {$gt: new Date() / 1000 - 1000}
                    },
                    sort: [{time: "desc"}],
                    limit: 200
                }
            }
        },
        watch: {
            h2s_grid: function (val) {
                let filter_time;
                filter_time = new Date() / 1000 - 500;
                this.h2s_collection = {
                    datasets: [
                        {
                            label: "concentration",
                            backgroundColor: 'rgba(3,169,244,0.3)',
                            data: val.filter(x => x.time > filter_time).map(x => ({x: x.time * 1000, y: x.data}))
                        }
                    ]
                };
            },
            nh3_grid: function (val) {
                let filter_time;
                filter_time = new Date() / 1000 - 500;
                this.nh3_collection = {
                    datasets: [
                        {
                            label: "concentration",
                            backgroundColor: 'rgba(3,169,244,0.3)',
                            data: val.filter(x => x.time > filter_time).map(x => ({x: x.time * 1000, y: x.data}))
                        }
                    ]
                };
            }
        }
    }
</script>

<style scoped>

    .sensor-graph {
        height: calc(30vh);
    }
</style>