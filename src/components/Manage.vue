<template>
    <v-container><p>{{ test }}</p>
        <v-dialog v-model="login_dialog" persistent max-width="290">
            <v-card>
                <v-toolbar
                        color="primary"
                        dark
                        flat
                >
                    <v-toolbar-title>Login</v-toolbar-title>
                </v-toolbar>
                <v-card-text>
                    <p>You are entering sudo mode. Only administrator can add/delete devices.</p>
                    <v-form>
                        <v-text-field
                                v-model="username"
                                label="Login"
                                name="login"
                                prepend-icon="person"
                                type="text"
                        />

                        <v-text-field
                                v-model="password"
                                id="password"
                                label="Password"
                                name="password"
                                prepend-icon="lock"
                                type="password"
                        />
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer/>
                    <v-btn color="primary" @click="login()">Login</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
    import axios from 'axios'

    export default {
        data() {
            return {
                username: "",
                password: "",
                login_dialog: false
            }
        },
        pouch: {
            test: {}
        },
        created() {
            axios.get("https://brownsense.misaka.center/db/_session").then((data) => {
                if (data.data.userCtx.name !== "admin") {
                    this.login_dialog = true;
                }
            });
            this.$pouch.pull("test", "https://brownsense.misaka.center/db/_users", {live: true});
        },
        methods: {
            login() {
                this.$pouch.connect(this.username, this.password, "https://brownsense.misaka.center/db/_users").then((val) => {
                    axios.get("https://brownsense.misaka.center/db/_session").then((data) => {
                        if (data.data.userCtx.name !== "admin") {
                            this.username = "";
                            this.password = "";
                        } else {
                            this.login_dialog = false;
                            this.$pouch.pull("test", "https://brownsense.misaka.center/db/_users", {live: true});
                        }
                    })
                })
            }
        },
        destroyed() {
            this.$pouch.close("test");
        }
    }
</script>

<style scoped>

</style>
