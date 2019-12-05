<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12" md="6">
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
            <v-col cols="12" md="6">
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
            <v-col cols="12" v-for="device in all_devs" :key="device.id">
                <v-skeleton-loader :loading="loading" type="card">
                    <device-summary :id="device.device" :mode="device.status" :actuator_raw="device.actuator"
                                    :h2s="device.h2s" :nh3="device.nh3"
                                    :enabled="online_devs.includes(device.device)"/>
                </v-skeleton-loader>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
    import {mapState} from 'vuex';
    import ClusterStatus from "./ClusterStatus";
    import ActuatorStatus from "./ActuatorStatus";
    import DeviceSummary from "./DeviceSummary";

    export default {
        data: () => ({
            timenow: 0,
            loading: true,
            db_summary: null
        }),
        components: {
            "cluster-status": ClusterStatus,
            "actuator-status": ActuatorStatus,
            "device-summary": DeviceSummary
        },
        pouch: {
            summary() {
                return {
                    database: this.dbs["summary"],
                    selector: {
                        device: {$gt: 0}
                    },
                    limit: 25
                }
            }
        },
        computed: {
            ...mapState([
                "dbs"
            ]),
            all_devs: function () {
                if (this.summary !== null) {
                    return this.summary.filter(x => x.device !== undefined).slice().sort((a, b) => a.device - b.device);
                } else {
                    return [];
                }
            },
            online_devs: function () {
                if (this.summary !== null) {
                    return this.summary.filter(
                        x => x.status !== "offline" && x.time > this.timenow - 10
                    ).map(x => x.device);
                } else {
                    return [];
                }
            },
            online: function () {
                if (this.summary !== null) {
                    return this.online_devs.length;
                } else {
                    return 0;
                }
            },
            lost: function () {
                if (this.summary !== null) {
                    return this.summary.filter(
                        x => x.status !== "offline" && x.time <= this.timenow - 10
                    ).length;
                } else {
                    return 0;
                }
            },
            offline: function () {
                if (this.summary !== null) {
                    return this.summary.filter(x => x.status === "offline").length;
                } else {
                    return 0;
                }
            },
            working: function () {
                if (this.summary !== null) {
                    return this.summary.filter(
                        x =>
                            x.status !== "offline" &&
                            x.time > this.timenow - 10 &&
                            x.actuator === true
                    ).length;
                } else {
                    return 0;
                }
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
            this.$store.commit("set_nav", [{text: "Overview", disabled: true}]);
            this.updatetime();
            this.$on("pouchdb-livefeed-ready", function () {
                this.loading = false;
            });
            setInterval(this.updatetime, 5000);
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