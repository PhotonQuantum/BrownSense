<template>
    <v-container>
        <v-layout wrap>
            <v-flex mb-5 xs12>
                <v-row justify="center">
                    <v-col cols="12" md="8">
                        <v-card>
                            <v-toolbar color="primary" dark>
                                <v-toolbar-title class="font-weight-light">Device Management</v-toolbar-title>
                                <v-spacer/>
                                <v-btn outlined class="font-weight-light" :disabled="loading"
                                       @click="()=>{this.new_device_name='';this.add_dialog=true}">Add Device
                                </v-btn>
                            </v-toolbar>
                            <v-card-text>
                                <v-skeleton-loader type="list-item, list-item, list-item" :loading="loading">
                                    <v-card outlined>
                                        <v-list class="pa-0">
                                            <div class="ma-0 pa-0" v-for="user in users" :key="user._id">
                                                <v-list-item :disabled="user.name === pending_delete.name">
                                                    <v-overlay color="white" opacity="1" absolute
                                                               :value="user.name === pending_delete.name">
                                                    </v-overlay>
                                                    <v-list-item-content>
                                                        <v-list-item-title
                                                                v-text="'Device #' + user.name.substring(7)"></v-list-item-title>
                                                    </v-list-item-content>
                                                    <v-list-item-action>
                                                        <v-btn icon @click="delete_device(user)">
                                                            <v-icon>mdi-delete</v-icon>
                                                        </v-btn>
                                                    </v-list-item-action>
                                                </v-list-item>
                                                <v-divider v-show="user !== users[users.length-1]"></v-divider>
                                            </div>
                                        </v-list>
                                    </v-card>
                                </v-skeleton-loader>
                            </v-card-text>
                        </v-card>
                        <v-dialog v-model="token_dialog" max-width="400">
                            <v-card>
                                <v-card-title>
                                    Device created
                                </v-card-title>
                                <v-card-text>
                                    <v-card outlined>
                                        <v-card-text>
                                            <p>
                                                <v-icon>mdi-api</v-icon>
                                                User: device_{{ new_device_name }}
                                            </p>
                                            <p>
                                                <v-icon>mdi-shield-lock</v-icon>
                                                Token: {{ new_device_token }}
                                            </p>
                                        </v-card-text>
                                    </v-card>
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer/>
                                    <v-btn text color="primary" @click="token_dialog = false">Close</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                        <v-dialog v-model="add_dialog" max-width="400">
                            <v-card>
                                <v-card-title>
                                    New device
                                </v-card-title>
                                <v-card-text>
                                    <v-form>
                                        <v-text-field
                                                v-model="new_device_name"
                                                label="Device name"
                                                name="new_device_name"
                                                prepend-icon="mdi-api"
                                                type="text"
                                        />
                                    </v-form>
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer/>
                                    <v-btn text color="primary" @click="create_device()">Create</v-btn>

                                </v-card-actions>
                            </v-card>
                        </v-dialog>
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
                        <v-snackbar :timeout='3000' v-model="delete_snackbar" @input="permanent_delete()">
                            Deleting {{ pending_delete.name }} ...
                            <v-btn color="pink" text @click="cancel_delete()">Undo</v-btn>
                            <v-btn color="pink" text @click="permanent_delete()">Close</v-btn>
                        </v-snackbar>
                    </v-col>
                </v-row>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import axios from 'axios'
    import PouchDB from 'pouchdb-browser'
    import uuid4 from 'uuid/v4'

    export default {
        data() {
            return {
                username: "",
                password: "",
                login_dialog: false,
                error_snackbar: false,
                error_snackbar_message: "",
                db_user: null,
                pending_delete: {},
                delete_snackbar: false,
                add_dialog: false,
                new_device_name: "",
                token_dialog: false,
                new_device_token: "",
                loading: true
            }
        },
        pouch: {
            users() {
                return {
                    database: this.db_user,
                    selector: {
                        name: {$regex: "device_.*"}
                    },
                    limit: 100
                }
            }
        },
        created() {
            axios.get("https://brownsense.misaka.center/db/_session").then((data) => {
                if (data.data.userCtx.name !== "admin") {
                    this.login_dialog = true;
                } else {
                    this.db_user = new PouchDB("https://brownsense.misaka.center/db/_users");
                    this.loading = false;
                }
            });
        },
        destroyed() {
            if (Object.keys(this.pending_delete).length !== 0) {
                this.permanent_delete();
            }
        },
        methods: {
            show_error(msg) {
                this.error_snackbar_message = msg;
                this.error_snackbar = true;
            },
            async create_device(user) {
                const new_device = "device_" + this.new_device_name;
                let create_user = false;
                try {
                    const result = await this.$pouch.get("org.couchdb.user:" + new_device, undefined, "https://brownsense.misaka.center/db/_users");
                } catch {
                    create_user = true;
                }
                if (create_user) {
                    this.new_device_token = uuid4().replace(/-/g, '');
                    const new_summary_id = uuid4().replace(/-/g, '');
                    const new_user = {
                        "_id": "org.couchdb.user:" + new_device,
                        "name": new_device,
                        "roles": ["devices"],
                        "type": "user",
                        "password": this.new_device_token
                    };
                    const new_summary = {
                        "_id": new_summary_id,
                        "device": this.new_device_name,
                        "time": 0,
                        "status": "offline",
                        "h2s": 0,
                        "nh3": 0,
                        "actuator": false
                    };
                    try {
                        await this.$pouch.put(new_user, undefined, "https://brownsense.misaka.center/db/_users");
                        await this.$pouch.put(new_summary, undefined, "https://brownsense.misaka.center/db/summary");
                        this.add_dialog = false;
                        this.token_dialog = true;
                    } catch {
                        this.show_error("Unexpected error.")
                    }
                } else {
                    this.new_device_name = "";
                    this.show_error("Device exists.")
                }
            },
            async permanent_delete() {
                const summary_item = await this.$pouch.find({selector: {device: this.pending_delete.name.substring(7)}}, "https://brownsense.misaka.center/db/summary");
                if (summary_item.docs.length > 0) {
                    await this.$pouch.remove(summary_item.docs[0], undefined, "https://brownsense.misaka.center/db/summary");
                }
                await this.$pouch.remove(this.pending_delete, undefined, "https://brownsense.misaka.center/db/_users");
                this.pending_delete = {};
                this.delete_snackbar = false;
            },
            async delete_device(user) {
                if (Object.keys(this.pending_delete).length !== 0) {
                    await this.permanent_delete();
                }
                this.pending_delete = user;
                this.delete_snackbar = true;
            },
            cancel_delete() {
                this.pending_delete = {};
                this.delete_snackbar = false;
            },
            login() {
                this.$pouch.connect(this.username, this.password, "https://brownsense.misaka.center/db/_users").then((val) => {
                    axios.get("https://brownsense.misaka.center/db/_session").then((data) => {
                        if (data.data.userCtx.name !== "admin") {
                            this.show_error("Authentication failed.")
                            this.username = "";
                            this.password = "";
                        } else {
                            this.login_dialog = false;
                            this.db_user = new PouchDB("https://brownsense.misaka.center/db/_users");
                            this.loading = false;
                        }
                    })
                })
            }
        }
    }
</script>

<style scoped>

</style>
