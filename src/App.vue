<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title class="headline" >
        <span>BrownSense</span>
      </v-toolbar-title>
        <template v-slot:extension>
          <v-tabs align-with-title background="transparent">
            <v-tab to="/summary">Overview</v-tab>
            <v-tab to="/detail">Details</v-tab>
            <v-tab to="/manage">Manage</v-tab>
            <v-tab to="/about">About</v-tab>
          </v-tabs>
        </template>
    </v-app-bar>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import PouchDB from 'pouchdb-browser';
import axios from 'axios'
export default {
  name: 'App',
  components: {
 //   HelloWorld,
  },
  data: () => ({
    //
  }),
  created: function(){
      this.connect_database();
  },
  methods: {
    async connect_database(){
      const session = await axios.get("https://brownsense.misaka.center/db/_session");
      if (session.data.userCtx.name === null) {
        await this.$pouch.connect("frontend_guest", "8696fee30cbd4a77814b4e8840676cea", "https://brownsense.misaka.center/db/summary");
      }
      this.$store.commit("add_db", {name: "summary", instance: new PouchDB("https://brownsense.misaka.center/db/summary")});
      this.$store.commit("add_db", {name: "datagrid", instance: new PouchDB("https://brownsense.misaka.center/db/datagrid")});
    }
  }
};
</script>
