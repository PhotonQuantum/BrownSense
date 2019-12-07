<template>
    <v-row justify="center">
        <v-col cols="12" md="6">
            <v-card hover outlined>
                <v-card-title class="text--secondary font-weight-light pb-2 pt-5"><span class="pl-3">Mode</span>
                </v-card-title>
                <v-card-text class="pb-5">
                    <span class="accent_data headline pl-4">{{ status }}</span>
                </v-card-text>
            </v-card>
        </v-col>
        <v-col cols="12" md="6">
            <v-card hover outlined>
                <v-card-title class="text--secondary font-weight-light pb-2 pt-5"><span class="pl-3">Actuator</span>
                </v-card-title>
                <v-card-text class="pb-5">
                    <span class="accent_data headline pl-4">{{ actuator }}</span>
                </v-card-text>
            </v-card>
        </v-col>
        <v-col cols="12" md="6">
            <v-card hover outlined>
                <v-row>
                    <v-col cols="6">
                        <v-card-title class="text--secondary font-weight-light pb-2 pt-5"><span class="pl-3">H2S</span>
                        </v-card-title>
                        <v-card-text class="pb-5">
                            <span class="accent_data headline pl-4">{{ this_device.h2s }} Units</span>
                        </v-card-text>
                    </v-col>
                    <v-col cols="6">
                        <v-sparkline :value="h2s_spark_array" class="ma-5" color="#1976d2" line-width="1.5" smooth="8" />
                    </v-col>
                </v-row>
            </v-card>
        </v-col>
        <v-col cols="12" md="6">
            <v-card hover outlined>
                <v-row>
                    <v-col cols="6">
                        <v-card-title class="text--secondary font-weight-light pb-2 pt-5"><span class="pl-3">NH3</span>
                        </v-card-title>
                        <v-card-text class="pb-5">
                            <span class="accent_data headline pl-4">{{ this_device.nh3 }} Units</span>
                        </v-card-text>
                    </v-col>
                    <v-col cols="6">
                        <v-sparkline :value="nh3_spark_array" class="ma-5" color="#1976d2" line-width="1.5" smooth="8" />
                    </v-col>
                </v-row>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
    import {mapState} from "vuex";

    export default {
        name: "DetailOverview",
        data: () => ({
            h2s_spark_array: [],
            nh3_spark_array: [],
            time_filter: -1,
            this_device: {h2s: "N/A", nh3: "N/A"}
        }),
        computed: {
            ...mapState([
                "dbs"
            ]),
            device: function () {
                return this.$route.params.id;
            },
            status: function () {
                if (this.this_device.status === "force_on" || this.this_device.status === "force_off") {
                    return "Manual";
                } else if (this.this_device.status === "offline") {
                    return "Offline";
                } else {
                    return "Automatic";
                }
            },
            actuator: function () {
                return this.this_device.actuator ? "Working" : "Stopped";
            },
        },
        watch: {
            h2s_grid: function(val){
                this.h2s_spark_array = val.slice(0, 10).reverse().map(x => (x.data))
            },
            nh3_grid: function(val){
                this.nh3_spark_array = val.slice(0, 10).reverse().map(x => (x.data))
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
                        time: {$gt: new Date() / 1000 - 3600}
                    },
                    sort: [{time: "desc"}],
                    limit: 100
                }
            },
            nh3_grid() {
                return {
                    database: this.dbs["datagrid"],
                    selector: {
                        device: this.device,
                        type: "nh3",
                        time: {$gt: new Date() / 1000 - 3600}
                    },
                    sort: [{time: "desc"}],
                    limit: 100
                }
            }
        }
    }
</script>

<style scoped>
    .accent_data {
        color: #1976d2 !important
    }
</style>