<template>
    <v-container>
        <v-layout text-center wrap>
            <v-flex mb-5 xs12>
                <v-row justify="center">
                    <v-col cols="12" md="8">
                        <v-skeleton-loader type="list-item, image" :loading="loading">
                            <v-card>
                                <v-card-title>
                                    <v-list-item two-line>
                                        <v-list-item-content>
                                            <v-list-item-subtitle>Hydrogen Sulfide</v-list-item-subtitle>
                                            <v-list-item-title class="headline">{{ this.this_device.h2s }} PPM
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
                                        ></line-chart>
                                    </div>
                                </v-card-text>
                            </v-card>
                        </v-skeleton-loader>
                    </v-col>
                    <v-col cols="12" md="8">
                        <v-skeleton-loader type="list-item, image" :loading="loading">
                            <v-card>
                                <v-card-title>
                                    <v-list-item two-line>
                                        <v-list-item-content>
                                            <v-list-item-subtitle>Ammonia</v-list-item-subtitle>
                                            <v-list-item-title class="headline">{{ this.this_device.nh3 }} PPM
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
                                        ></line-chart>
                                    </div>
                                </v-card-text>
                            </v-card>
                        </v-skeleton-loader>
                    </v-col>
                </v-row>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import LineChart from "./LineChart.js";
    import PouchDB from 'pouchdb-browser';
    import VueScreenSize from 'vue-screen-size';

    export default {
        mixins: [VueScreenSize.VueScreenSizeMixin],
        data: () => ({
            loading: true,
            h2s_collection: null,
            nh3_collection: null,
            time_filter: -1,
            db_summary: null
        }),
        components: {LineChart},
        props: ["device"],
        computed: {
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
            /*
            dev_one() {
              return {
                database: "datagrid",
                selector: this.db_selector,
                sort: [{ time: "asc" }]
              };
            }
            */
            this_device() {
                return {
                    database: this.db_summary,
                    selector: {
                        device: this.device
                    },
                    first: true
                }
            },
            h2s_grid() {
                return {
                    database: this.db_datagrid,
                    selector: {
                        device: this.device,
                        type: "h2s",
                        time: {$gt: this.time_filter - 1000}
                    },
                    sort: [{time: "desc"}],
                    limit: 200
                }
            },
            nh3_grid() {
                return {
                    database: this.db_datagrid,
                    selector: {
                        device: this.device,
                        type: "nh3",
                        time: {$gt: this.time_filter - 1000}
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
        },

        created: function () {
            this.loaded = false;
            this.time_filter = new Date() / 1000;
            this.db_datagrid = new PouchDB("https://brownsense.misaka.center/db/datagrid");
            this.db_summary = new PouchDB("https://brownsense.misaka.center/db/summary");
            // this.$pouch.sync("dev_one", "https://brownsense.misaka.center/db/test");
            this.$on("pouchdb-livefeed-ready", function () {
                this.loading = false;
            });
        }
    };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    h3 {
        margin: 40px 0 0;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        display: inline-block;
        margin: 0 10px;
    }

    a {
        color: #42b983;
    }

    .sensor-graph {
        height: calc(30vh);
    }
</style>
