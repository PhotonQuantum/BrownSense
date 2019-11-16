<template>
    <v-container>
        <v-layout wrap>
            <v-flex mb-4>
                <v-row justify="center">
                    <v-col cols="12" md="4">
                        <v-skeleton-loader :loading="loading" type="card-heading, image">
                        <v-card>
                            <v-card-title class="text-uppercase">
                                <span class="font-weight-light">cluster status</span>
                            </v-card-title>
                            <div class="graph">
                                <cluster-status :online="online" :offline="offline" :lost="lost"></cluster-status>
                            </div>
                        </v-card>
                        </v-skeleton-loader>
                    </v-col>
                    <v-col cols="12" md="4">
                        <v-skeleton-loader :loading="loading" type="card-heading, image">
                        <v-card>
                            <v-card-title class="text-uppercase">
                                <span class="font-weight-light">actuator status</span>
                            </v-card-title>
                            <div class="graph">
                                <actuator-status :working="working" :pending="pending"></actuator-status>
                            </div>
                        </v-card>
                        </v-skeleton-loader>
                    </v-col>
                </v-row>
                <v-row justify="center">
                    <v-col cols="12" md="8" v-for="device in all_devs" :key="device.id">
                        <v-skeleton-loader :loading="loading" type="card">
                        <device-summary :id="device.device" :mode="device.status" :actuator_raw="device.actuator"
                                        :h2s="device.h2s" :nh3="device.nh3" :enabled="online_devs.includes(device.device)"></device-summary>
                        </v-skeleton-loader>
                    </v-col>
                </v-row>
            </v-flex>
        </v-layout>
    </v-container>
</template>
<script>
    import PouchDB from "pouchdb-browser";
    import ClusterStatus from "./ClusterStatus";
    import ActuatorStatus from "./ActuatorStatus";
    import DeviceSummary from "./DeviceSummary";

    export default {
        data: () => ({
            timenow: 0,
            summary: [],
            loading: true
        }),
        components: {
            "cluster-status": ClusterStatus,
            "actuator-status": ActuatorStatus,
            "device-summary": DeviceSummary
        },
        pouch: {
            summary: {}
        },
        computed: {
            all_devs: function () {
                return this.summary.filter(x => x.device !== undefined).slice().sort((a, b) => a.device - b.device);
            },
            online_devs: function () {
                return this.summary.filter(
                    x => x.status !== "offline" && x.time > this.timenow - 10
                ).map(x=>x.device);
            },
            online: function () {
                return this.online_devs.length;
            },
            lost: function () {
                return this.summary.filter(
                    x => x.status !== "offline" && x.time <= this.timenow - 10
                ).length;
            },
            offline: function () {
                return this.summary.filter(x => x.status === "offline").length;
            },
            working: function () {
                return this.summary.filter(
                    x =>
                        x.status !== "offline" &&
                        x.time > this.timenow - 10 &&
                        x.actuator === true
                ).length;
            },
            pending: function () {
                return this.online - this.working;
            }
        },
        methods: {
            updatetime: function () {
                this.timenow = new Date() / 1000;
            }
        },
        created: function () {
            this.updatetime();
            this.$pouch.pull("summary", "http://localhost:5984/summary", {
                live: true
            });
            this.$on("pouchdb-pull-change", function (){
                this.loading = false;
            });
            setInterval(this.updatetime, 5000);
        },
        destroyed: function () {
            this.$pouch.close("summary");
        }
    };
</script>
<style scoped>
    .graph {
        max-width: 300px;
        margin: 0 auto;
        padding-bottom: 20px;
    }
</style>