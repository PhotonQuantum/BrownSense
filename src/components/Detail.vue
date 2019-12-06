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
                    <v-overlay :value="!is_sudo" absolute class="justify-center" opacity=".6">
                        <v-alert v-if="!is_sudo" dense type="warning" dark>Sudoer only.</v-alert>
                        <div class="text-center"><v-btn text @click="()=>{this.login_admin=false; this.login_dialog=true;}">Login</v-btn></div>
                    </v-overlay>
                    <v-card-title>
                        <v-icon left>mdi-information</v-icon>
                        <span class="title font-weight-light">Override</span>
                    </v-card-title>

                    <v-card-text class="pb-0">
                        <v-radio-group class="ma-0 pa-0" v-model="override_mode" mandatory>
                            <v-radio label="Auto" value="auto"/>
                            <v-radio label="Force On" value="force_on"/>
                            <v-radio label="Force Off" value="force_off"/>
                        </v-radio-group>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer/>
                        <v-btn text @click="menu_switch = false">Cancel</v-btn>
                        <v-btn color="primary" text @click="set_override">Apply</v-btn>
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
                    <v-overlay :value="!is_admin" absolute class="justify-center" opacity=".6">
                        <v-alert v-if="!is_admin" dense type="warning" dark>Admin only.</v-alert>
                        <div class="text-center"><v-btn text @click="()=>{this.login_admin=true; this.login_dialog=true;}">Login</v-btn></div>
                    </v-overlay>
                    <v-card-title>
                        <v-icon color="error" left>mdi-alert-circle</v-icon>
                        <span class="title font-weight-light error--text">Delete</span>
                    </v-card-title>

                    <v-card-text class="pb-0">
                        <span>Are you sure you want to delete this device?</span>
                        <v-checkbox v-model="delete_confirm" label="Yes, delete this device."/>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer/>
                        <v-btn text @click="()=>{this.menu_delete = false; this.delete_confirm = false;}">Cancel</v-btn>
                        <v-btn color="error" text @click="deleteDevice"
                               :disabled="!delete_confirm">Delete
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-menu>
        </v-toolbar>
        <v-tabs background-color="transparent">
            <v-tab to="overview">Overview</v-tab>
            <v-tab to="graph">Graph</v-tab>
        </v-tabs>
        <v-divider/>
        <router-view/>
        <v-dialog v-model="login_dialog" max-width="400">
            <v-card>
                <v-card-title>
                    Authentication Required
                </v-card-title>
                <v-card-text>
                    <v-alert dense outlined type="warning">You are entering sudo mode.</v-alert>
                    <v-form>
                        <v-text-field
                                v-model="username"
                                label="Login"
                                name="login"
                                prepend-icon="mdi-account"
                                type="text"
                                ref="text_username"
                        />

                        <v-text-field
                                v-model="password"
                                id="password"
                                label="Password"
                                name="password"
                                prepend-icon="mdi-lock"
                                type="password"
                                @keyup.enter.native="login()"
                        />
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer/>
                    <v-btn text color="primary" @click="login()">Login</v-btn>

                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar :timeout='3000' color="error" v-model="error_snackbar">
            {{ error_snackbar_message }}
            <v-btn text @click="error_snackbar = false">Close</v-btn>
        </v-snackbar>
    </v-container>
</template>

<script>
    import axios from "axios";
    import PouchDB from "pouchdb-browser";
    import {mapState} from 'vuex';
    import uuid4 from 'uuid/v4'

    export default {
        data: () => ({
            menu_switch: false,
            menu_delete: false,
            delete_confirm: false,
            is_sudo: false,
            is_admin: false,
            login_dialog: false,
            login_admin: false,
            username: "",
            password: "",
            error_snackbar: false,
            error_snackbar_message: "",
            override_mode: "auto"
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
        },
        methods:{
            deleteDevice: async function(){
                const summary_item = await this.dbs["summary"].find({selector: {device: this.device}});
                if (summary_item.docs.length > 0) {
                    await this.dbs["summary"].remove(summary_item.docs[0]);
                }
                const user_item = await this.dbs["users"].get("org.couchdb.user:device_" + this.device);
                await this.dbs["users"].remove(user_item);
                await this.$router.push("/");
            },
            validateUser: async function(validateAdmin=false){
                const session = await axios.get("https://brownsense.misaka.center/db/_session");
                this.is_sudo = session.data.userCtx.roles.includes("sudoers") || session.data.userCtx.roles.includes("_admin");
                this.is_admin = session.data.userCtx.roles.includes("_admin");
                if (this.is_sudo){
                    this.$store.commit("add_db", {
                        name: "command",
                        instance: new PouchDB("https://brownsense.misaka.center/db/command")
                    });
                }
                if (this.is_admin){
                    this.$store.commit("add_db", {
                        name: "users",
                        instance: new PouchDB("https://brownsense.misaka.center/db/_users")
                    })
                }
                return (validateAdmin?this.is_admin:this.is_sudo);
            },
            login: async function(){
                await this.$pouch.connect(this.username, this.password, "https://brownsense.misaka.center/db/command");
                const is_sudo = await this.validateUser(this.login_admin);
                if (is_sudo){
                    this.username = "";
                    this.password = "";
                    this.login_dialog = false;
                } else {
                    this.show_error("Authentication failed.");
                    this.username = "";
                    this.password = "";
                    this.$refs['text_username'].focus();
                }
            },
            show_error(msg) {
                this.error_snackbar_message = msg;
                this.error_snackbar = true;
            },
            async set_override(){
                this.menu_switch = false;
                await this.send_command({event: "override", data: this.override_mode})
            },
            async send_command(payload){
                const doc_id = uuid4().replace(/-/g, '');
                const data = {_id: doc_id, type: "task", device: this.device, created_at: new Date()/1000,  payload: payload};
                await this.dbs["command"].put(data);
            }
        },
        created: function () {
            this.$store.commit("set_nav", [{text: "Overview", disabled: false, to: "/"}, {
                text: "Device #" + this.device,
                disabled: true
            }]);
            this.validateUser();
        },
    };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
