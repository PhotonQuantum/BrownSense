<template>
  <v-container>
    <v-layout text-center wrap>
      <v-flex mb-4>
        <p>This is summary page.</p>
        <p>{{ all_devs }}</p>
        <v-row justify="center">
          <v-col cols="12" md="4">
            <v-card>
              <v-card-title class="text-uppercase">
                <span class="font-weight-light">cluster status</span>
              </v-card-title>
              <div class="graph">
                <cluster-status :online="online" :offline="offline" :lost="lost"></cluster-status>
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card>
              <v-card-title class="text-uppercase">
                <span class="font-weight-light">actuator status</span>
              </v-card-title>
              <div class="graph">
                <actuator-status :working="working" :pending="pending"></actuator-status>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import PouchDB from "pouchdb-browser";
import ClusterStatus from "./ClusterStatus";
import ActuatorStatus from "./ActuatorStatus";
export default {
  data: () => ({
    timenow: 0,
    summary: []
  }),
  components: {
    "cluster-status": ClusterStatus,
    "actuator-status": ActuatorStatus
  },
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
    },
    working: function() {
      return this.summary.filter(
        x =>
          x.status != "offline" &&
          x.time > this.timenow - 10 &&
          x.actuator == true
      ).length;
    },
    pending: function() {
      return this.online - this.working;
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
<style scoped>
.graph {
  width: 300px;
  margin: 0 auto;
  padding-bottom: 20px;
}
</style>