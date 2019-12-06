<template>
    <v-card :disabled="!enabled" hover>
        <v-card-title class="text-uppercase">
            <span class="font-weight-light">Device #{{ id }}</span>
        </v-card-title>
        <v-card-text>
            <v-row>
                <v-col cols="6">
                    <v-list-item>
                        <v-list-item-icon>
                            <v-icon>mdi-console-line</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title class="text-uppercase">{{ status }}</v-list-item-title>
                    </v-list-item>
                </v-col>
                <v-col cols="6">
                    <v-list-item>
                        <v-list-item-icon>
                            <v-icon>mdi-fan</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title class="text-uppercase">{{ actuator }}</v-list-item-title>
                    </v-list-item>
                </v-col>
            </v-row>
            <div v-if="enabled">
            <v-divider></v-divider>
            <v-row align="center">
                <v-col cols="12" md="6">
                    <v-list class="transparent">
                        <v-list-item>
                            <v-list-item-title>H2S</v-list-item-title>
                            <v-list-item-icon class="text-center">
                                <v-icon v-if="this.h2s <= 40">mdi-check-circle</v-icon>
                                <v-icon v-else>mdi-alert-circle</v-icon>
                            </v-list-item-icon>
                            <v-list-item-subtitle class="text-right">{{ h2s }}ppm</v-list-item-subtitle>
                        </v-list-item>
                    </v-list>
                    <v-col cols="12">
                        <v-progress-linear :value="progress_h2s" :color="color_h2s"></v-progress-linear>
                    </v-col>
                </v-col>
                <v-col cols="12" md="6">
                    <v-list class="transparent">
                        <v-list-item>
                            <v-list-item-title>NH3</v-list-item-title>
                            <v-list-item-icon class="text-center">
                                <v-icon v-if="this.nh3 <= 40">mdi-check-circle</v-icon>
                                <v-icon v-else>mdi-alert-circle</v-icon>
                            </v-list-item-icon>
                            <v-list-item-subtitle class="text-right">{{ nh3 }}ppm</v-list-item-subtitle>
                        </v-list-item>
                    </v-list>
                    <v-col cols="12">
                        <v-progress-linear :value="progress_nh3" :color="color_nh3"></v-progress-linear>
                    </v-col>
                </v-col>
            </v-row></div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
            <v-btn :to="detail_url" class="text-uppercase" text>details</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
    export default {
        name: "device-summary",
        props: ["id", "enabled", "mode", "actuator_raw", "h2s", "nh3"],
        computed: {
            detail_url: function(){
                return "device/" + this.id;
            },
            status: function() {
                if (this.mode === "force_on" || this.mode === "force_off"){
                    return "manual";
                } else if (!this.enabled) {
                    return "offline";
                } else {
                    return "automatic";
                }
            },
            actuator: function() {
                if (this.enabled){
                    return this.actuator_raw?"on":"off";
                } else {
                    return "N/A";
                }
            },
            progress_nh3: function() {
                return this.nh3 / 80 * 100;
            },
            progress_h2s: function() {
                return this.h2s / 80 * 100;
            },
            color_nh3: function(){
                return this.nh3 > 40?"orange":"light-blue";
            },
            color_h2s: function(){
                return this.h2s > 40?"orange":"light-blue";
            }
        }
    }
</script>

<style scoped>

</style>