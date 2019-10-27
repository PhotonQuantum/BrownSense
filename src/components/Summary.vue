<template>
  <v-container>
    <p>This is summary page.</p>
    <p>online: {{ online }} offline: {{ offline }} lost: {{ lost }}</p>
    <p>{{ all_devs }}</p>
  </v-container>
</template>
<script>
import PouchDB from "pouchdb-browser";
export default {
  data: () => ({
    timenow: 0,
    summary: []
  }),
  pouch: {
    summary: {}
  },
  computed: {
    all_devs: function() {
      return this.summary.filter(x => x.device != undefined).map(x => x.device);
    },
    online: function() {
      return this.summary.filter(
        x => x.status != "offline" && x.time > this.timenow - 10
      ).length;
    },
    lost: function() {
      return this.summary.filter(
        x => x.status != "offline" && x.time <= this.timenow - 10
      ).length;
    },
    offline: function() {
      return this.summary.filter(x => x.status == "offline").length;
    }
  },
  methods: {
    updatetime: function() {
      this.timenow = new Date() / 1000;
    }
  },
  created: function() {
    this.updatetime();
    this.$pouch.pull("summary", "http://localhost:5984/summary", {
      live: true
    });
    setInterval(this.updatetime, 5000);
  },
  destroyed: function() {
    this.$pouch.close("summary");
  }
};
</script>