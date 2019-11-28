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
// import HelloWorld from './components/HelloWorld';
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
    axios.get("https://brownsense.misaka.center/db/_session").then((data) => {
      if (data.data.userCtx.name === null) {
        this.$pouch.connect("frontend_guest", "8696fee30cbd4a77814b4e8840676cea", "https://brownsense.misaka.center/db/summary").then((data) => {
          this.$router.go();
        });
      }
    });
  }
};
</script>
