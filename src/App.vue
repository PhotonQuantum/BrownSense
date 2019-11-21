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

export default {
  name: 'App',
  components: {
 //   HelloWorld,
  },
  data: () => ({
    //
  }),
};
</script>
