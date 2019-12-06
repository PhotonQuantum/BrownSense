<!--suppress JSUnresolvedVariable -->
<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12">
                <v-card>
                    <v-toolbar color="primary" dark elevation="0">
                        <v-toolbar-title class="font-weight-light">Device Management</v-toolbar-title>
                        <v-spacer/>
                        <v-btn outlined class="font-weight-light" :disabled="loading"
                               @click="()=>{this.new_device_name='';this.add_dialog=true}">Add Device
                        </v-btn>
                    </v-toolbar>
                    <v-card-text>
                        <v-skeleton-loader type="list-item, list-item, list-item" :loading="loading">
                            <v-card outlined :disabled="deleting">
                                <v-list class="pa-0">
                                    <div class="ma-0 pa-0" v-for="user in users" :key="user._id">
                                        <v-list-item :disabled="user.name === pending_delete.name">
                                            <v-overlay color="white" opacity="1" absolute
                                                       :value="user.name === pending_delete.name">
                                            </v-overlay>
                                            <v-list-item-content>
                                                <v-list-item-title
                                                        v-text="'Device #' + user.name.substring(7)"/>
                                            </v-list-item-content>
                                            <v-list-item-action>
                                                <v-btn icon @click="delete_device(user)">
                                                    <v-icon>mdi-delete</v-icon>
                                                </v-btn>
                                            </v-list-item-action>
                                        </v-list-item>
                                        <v-divider v-show="user !== users[users.length-1]"/>
                                    </div>
                                </v-list>
                            </v-card>
                        </v-skeleton-loader>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="12">
                <v-card>
                    <v-toolbar color="primary" dark elevation="0">
                        <v-toolbar-title class="font-weight-light">Database Operation</v-toolbar-title>
                    </v-toolbar>
                    <v-skeleton-loader type="list-item" :loading="loading">
                        <v-card-actions>
                            <v-btn @click="clean_datagrid()">Clean Datagrid</v-btn>
                            <v-btn @click="compact_database()">Compact Database</v-btn>
                        </v-card-actions>
                    </v-skeleton-loader>
                </v-card>
            </v-col>
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
                <v-card :disabled="creating_device">
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
            <v-snackbar :timeout='3000' v-model="delete_snackbar" @input="permanent_delete()">
                Deleting {{ pending_delete.name }} ...
                <v-btn color="pink" text @click="cancel_delete()">Undo</v-btn>
                <v-btn color="pink" text @click="permanent_delete()">Close</v-btn>
            </v-snackbar>
            <v-overlay :value="working">
                <div class="text-center">
                    <h1 class="text--white font-weight-light text-uppercase">{{ working_title }}</h1>
                    <v-progress-circular :indeterminate="working_indeterminate" :rotate="working_rotate"
                                         size="90" :value="working_value">{{ working_msg }}
                    </v-progress-circular>
                </div>
            </v-overlay>
        </v-row>
    </v-container>
</template>

<script>
    import axios from 'axios'
    import {mapState} from 'vuex'
    import PouchDB from 'pouchdb-browser'
    import uuid4 from 'uuid/v4'

    export default {
        data() {
            return {
                deleting: false,
                working: false,
                working_indeterminate: false,
                working_value: 0,
                working_rotate: 0,
                working_msg: "",
                working_title: "",
                creating_device: false,
                username: "",
                password: "",
                login_dialog: false,
                error_snackbar: false,
                error_snackbar_message: "",
                pending_delete: {},
                delete_snackbar: false,
                add_dialog: false,
                new_device_name: "",
                token_dialog: false,
                new_device_token: "",
                loading: true
            }
        },
        computed: mapState([
            "dbs"
        ]),
        pouch: {
            users() {
                return {
                    database: this.dbs["users"],
                    selector: {
                        name: {$regex: "device_.*"}
                    },
                    limit: 100
                }
            }
        },
        created() {
            this.$store.commit("set_nav", [{text: "Manage", disabled: true}]);
            axios.get("https://brownsense.misaka.center/db/_session").then((data) => {
                if (data.data.userCtx.name !== "admin") {
                    this.login_dialog = true;
                } else {
                    this.$store.commit("add_db", {
                        name: "users",
                        instance: new PouchDB("https://brownsense.misaka.center/db/_users")
                    });
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
            async create_device() {
                const new_device = "device_" + this.new_device_name;
                this.creating_device = true;
                let create_user = false;
                try {
                    await this.dbs["users"].get("org.couchdb.user:" + new_device);
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
                        await this.dbs["users"].put(new_user);
                        await this.dbs["summary"].put(new_summary);
                        this.add_dialog = false;
                        this.token_dialog = true;
                        this.creating_device = false;
                    } catch {
                        this.show_error("Unexpected error.");
                        this.new_device_name = "";
                        this.add_dialog = false;
                        this.creating_device = false;
                    }
                } else {
                    this.new_device_name = "";
                    this.show_error("Device exists.");
                    this.creating_device = false;
                }
            },
            async permanent_delete() {
                this.deleting = true;
                this.delete_snackbar = false;
                const summary_item = await this.dbs["summary"].find({selector: {device: this.pending_delete.name.substring(7)}});
                if (summary_item.docs.length > 0) {
                    await this.dbs["summary"].remove(summary_item.docs[0]);
                }
                await this.dbs["users"].remove(this.pending_delete);
                this.pending_delete = {};
                this.deleting = false;
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
            async login() {
                await this.$pouch.connect(this.username, this.password, "https://brownsense.misaka.center/db/_users")
                const data = await axios.get("https://brownsense.misaka.center/db/_session")
                if (data.data.userCtx.name !== "admin") {
                    this.show_error("Authentication failed.");
                    this.username = "";
                    this.password = "";
                    this.$refs['text_username'].focus();
                } else {
                    this.login_dialog = false;
                    this.$store.commit("add_db", {
                        name: "users",
                        instance: new PouchDB("https://brownsense.misaka.center/db/_users")
                    });
                    this.loading = false;
                }
            },
            async compact_database() {
                this.working_title = "compacting database";
                this.working_rotate = 0;
                this.working_indeterminate = true;
                this.working_value = 0;
                this.working_msg = "";
                this.working = true;
                await this.dbs["summary"].compact();
                // await this.dbs["command"].compact();
                await this.dbs["datagrid"].compact();
                this.working_title = "complete";
                this.working_indeterminate = false;
                this.working_value = 100;
                await new Promise(resolve => setTimeout(resolve, 1000));
                this.working = false;
            },
            async clean_datagrid() {
                this.working_title = "cleaning database";
                this.working_rotate = -90;
                this.working_indeterminate = false;
                this.working_value = 0;
                this.working = true;
                const total = (await this.dbs["datagrid"].info()).doc_count;
                let datalist = await this.dbs["datagrid"].allDocs({limit: 1});
                const valid_devices = this.users.map((x) => (x.name.substring(7)));
                let purge_list = {};
                if (datalist.rows.length > 0) {
                    let startkey = datalist.rows[0].id;
                    let finished = false;
                    let counter = 0;
                    while (!finished) {
                        datalist = await this.dbs["datagrid"].allDocs({
                            startkey: startkey,
                            limit: 101,
                            include_docs: true
                        });
                        this.working_value = Math.floor(counter / total * 100);
                        this.working_msg = this.working_value;
                        datalist.rows.slice(0, -1).forEach((row) => {
                            if (!valid_devices.includes(row.doc.device) && row.doc._id.substring(0, 8) !== "_design/") {
                                purge_list[row.doc._id] = [row.doc._rev];
                            }
                        });
                        await axios.post('/db/datagrid/_purge', purge_list);
                        purge_list = {};
                        startkey = datalist.rows[datalist.rows.length - 1].id;
                        counter += 100;
                        finished = datalist.rows.length < 101;
                    }
                    const row = datalist.rows[datalist.rows.length - 1];
                    if (!valid_devices.includes(row.doc.device) && row.doc._id.substring(0, 8) !== "_design/") {
                        purge_list[row.doc._id] = [row.doc._rev];
                        await axios.post('/db/datagrid/_purge', purge_list);
                    }
                }
                this.working_title = "complete";
                this.working_value = 100;
                this.working_msg = this.working_value;
                await new Promise(resolve => setTimeout(resolve, 1000));
                this.working = false;
            }
        }
    }
</script>

<style scoped>

</style>
