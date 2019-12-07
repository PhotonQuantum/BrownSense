<template>

    <v-row justify="center">
        <v-col cols="12">
            <v-col cols="12" sm="6">
                <v-select
                        :items="graph_types"
                        v-model="graph_select"
                        label="Range"
                        hide-details
                        outlined
                />
            </v-col>
        </v-col>
        <v-col cols="12">
            <v-card>
                <v-card-title>
                    <v-list-item two-line>
                        <v-list-item-content class="text-center">
                            <v-list-item-subtitle>Hydrogen Sulfide</v-list-item-subtitle>
                            <v-list-item-title class="headline">{{ this_device.h2s }} Units
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-card-title>
                <v-card-text>
                    <div class="grey lighten-4 pa-6">
                        <line-chart
                                v-show="graph_select === 'Last hour'"
                                class="sensor-graph"
                                :chart-data="h2s_minutely"
                                :options="chart_options"
                        />
                        <line-chart
                                v-show="graph_select !== 'Last hour'"
                                class="sensor-graph"
                                :chart-data="h2s_hourly"
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
                            <v-list-item-title class="headline">{{ this_device.nh3 }} Units
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-card-title>
                <v-card-text>
                    <div class="grey lighten-4 pa-6">
                        <line-chart
                                v-show="graph_select === 'Last hour'"
                                class="sensor-graph"
                                :chart-data="nh3_minutely"
                                :options="chart_options"
                        />
                        <line-chart
                                v-show="graph_select !== 'Last hour'"
                                class="sensor-graph"
                                :chart-data="nh3_hourly"
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
            h2s_minutely: {},
            nh3_minutely: {},
            h2s_hourly: {},
            nh3_hourly: {},
            this_device: {h2s: "N/A", nh3: "N/A"},
            graph_types: ["Last hour", "Last 3 days"],
            graph_select: "Last hour"
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
            h2s_minutely_raw() {
                return {
                    database: this.dbs["datagrid"],
                    selector: {
                        device: this.device,
                        type: "h2s",
                        graph: "minutely",
                        time: {$gt: new Date() / 1000 - 3600}
                    },
                    sort: [{time: "desc"}],
                    limit: 100
                }
            },
            nh3_minutely_raw() {
                return {
                    database: this.dbs["datagrid"],
                    selector: {
                        device: this.device,
                        type: "nh3",
                        graph: "minutely",
                        time: {$gt: new Date() / 1000 - 3600}
                    },
                    sort: [{time: "desc"}],
                    limit: 100
                }
            },
            h2s_hourly_raw() {
                return {
                    database: this.dbs["datagrid"],
                    selector: {
                        device: this.device,
                        type: "h2s",
                        graph: "hourly",
                        time: {$gt: new Date() / 1000 - 259200}
                    },
                    sort: [{time: "desc"}],
                    limit: 100
                }
            },
            nh3_hourly_raw() {
                return {
                    database: this.dbs["datagrid"],
                    selector: {
                        device: this.device,
                        type: "nh3",
                        graph: "hourly",
                        time: {$gt: new Date() / 1000 - 259200}
                    },
                    sort: [{time: "desc"}],
                    limit: 100
                }
            }
        },
        watch: {
            h2s_minutely_raw: function (val) {
                let filter_time;
                filter_time = new Date() / 1000 - 3600;
                this.h2s_minutely = {
                    datasets: [
                        {
                            label: "concentration",
                            backgroundColor: 'rgba(3,169,244,0.3)',
                            data: val.filter(x => x.time > filter_time).map(x => ({x: x.time * 1000, y: x.data}))
                        }
                    ]
                };
            },
            nh3_minutely_raw: function (val) {
                let filter_time;
                filter_time = new Date() / 1000 - 3600;
                this.nh3_minutely = {
                    datasets: [
                        {
                            label: "concentration",
                            backgroundColor: 'rgba(3,169,244,0.3)',
                            data: val.filter(x => x.time > filter_time).map(x => ({x: x.time * 1000, y: x.data}))
                        }
                    ]
                };
            },
            h2s_hourly_raw: function (val) {
                let filter_time;
                filter_time = new Date() / 1000 - 259200;
                this.h2s_hourly = {
                    datasets: [
                        {
                            label: "concentration",
                            backgroundColor: 'rgba(3,169,244,0.3)',
                            data: val.filter(x => x.time > filter_time).map(x => ({x: x.time * 1000, y: x.data}))
                        }
                    ]
                };
            },
            nh3_hourly_raw: function (val) {
                let filter_time;
                filter_time = new Date() / 1000 - 259200;
                this.nh3_hourly = {
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