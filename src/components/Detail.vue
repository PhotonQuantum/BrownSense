<template>
    <v-container>
        <v-toolbar flat class="transparent">
            <v-icon large color="primary">mdi-raspberry-pi</v-icon>
            <v-toolbar-title class="headline font-weight-light text-wrap" style="padding-left: 20px">
                Device Information (Device #{{device}})
            </v-toolbar-title>
            <v-spacer/>

            <v-menu
                    v-model="menu_switch"
                    :close-on-content-click="false"
                    :nudge-width="200"
                    offset-y
            >
                <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on">
                        <v-icon size="28">mdi-toggle-switch-off</v-icon>
                    </v-btn>
                </template>

                <v-card>
                    <v-card-title>
                        <v-icon left>mdi-information</v-icon>
                        <span class="title font-weight-light">Override</span>
                    </v-card-title>

                    <v-card-text style="padding-bottom: 0">
                        <v-radio-group>
                            <v-radio label="Auto"/>
                            <v-radio label="Force On"/>
                            <v-radio label="Force Off"/></v-radio-group>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer />
                        <v-btn text @click="menu_switch = false">Cancel</v-btn>
                        <v-btn color="primary" text @click="menu_switch = false">Apply</v-btn>
                    </v-card-actions>
                </v-card>
            </v-menu>

            <v-menu
                    v-model="menu_delete"
                    :close-on-content-click="false"
                    :nudge-width="200"
                    offset-y
            >
                <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on">
                        <v-icon size="28">mdi-delete</v-icon>
                    </v-btn>
                </template>

                <v-card>
                    <v-card-title>
                        <v-icon color="error" left>mdi-alert-circle</v-icon>
                        <span class="title font-weight-light error--text">Delete</span>
                    </v-card-title>

                    <v-card-text style="padding-bottom: 0">
                        <span>Are you sure you want to delete this device?</span>
                        <v-checkbox v-model="delete_confirm" label="Yes, delete this device."/>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer />
                        <v-btn text @click="menu_delete = false">Cancel</v-btn>
                        <v-btn color="error" text @click="menu_delete = false" :disabled="!delete_confirm">Delete</v-btn>
                    </v-card-actions>
                </v-card>
            </v-menu>
        </v-toolbar>
        <v-tabs background-color="transparent">
            <v-tab to="overview">Overview</v-tab>
            <v-tab to="graph">Graph</v-tab>
        </v-tabs>
        <v-divider />
        <router-view />
    </v-container>
</template>

<script>
    import {mapState} from 'vuex';

    export default {
        data: () => ({
            menu_switch: false,
            menu_delete: false,
            delete_confirm: false
        }),
        computed: {
            ...mapState([
                "dbs"
            ]),
            device: function () {
                return this.$route.params.id;
            },
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
                    database: this.dbs["summary"],
                    selector: {
                        device: this.device
                    },
                    first: true
                }
            },
        },
        watch: {
            this_device: function (val) {
                if (val.device === undefined) {
                    this.$router.replace("/404");
                }
            },
        },

        created: function () {
            this.$store.commit("set_nav", [{text: "Overview", disabled: false, to: "/"}, {
                text: "Device #" + this.device,
                disabled: true
            }]);
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

</style>
