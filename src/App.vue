<template>
  <v-app>
      <v-navigation-drawer app v-model="drawer_open" color="primary" dark>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title">
              BrownSense
            </v-list-item-title>
            <v-list-item-subtitle>
              Toilet IAQ Monitor
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-divider />
        <v-list dense nav>
          <v-list-item
                  v-for="item in drawer"
                  :key="item.title"
                  link
                  :to="item.to"
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
              </v-list-item>
        </v-list>
      </v-navigation-drawer>

    <v-app-bar app v-model="this.$vuetify.breakpoint.mdAndDown" color="primary" dark>
        <v-app-bar-nav-icon @click="drawer_open = !drawer_open"/>
      <v-toolbar-title class="headline" >
        <span>BrownSense</span>
      </v-toolbar-title>
    </v-app-bar>

    <v-content>
      <v-container>
        <v-layout wrap>
          <v-flex mb-4>
            <v-row justify="center">
              <v-col cols="12" md="10" class="pa-0">
                <v-breadcrumbs :items="bread_nav" divider=">"/>
                <router-view />
              </v-col>
            </v-row>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import PouchDB from 'pouchdb-browser';
import axios from 'axios'
import {mapState} from 'vuex'

export default {
  name: 'App',
  components: {
 //   HelloWorld,
  },
  computed: mapState([
    "bread_nav"
  ]),
  data: () => ({
      drawer:[
        {title: "Overview", icon: "mdi-view-dashboard", to: "/"},
        {title: "Manage", icon: "mdi-settings", to: "/manage"},
        {title: "About", icon: "mdi-information", to: "/about"}
      ],
      drawer_open: null
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
