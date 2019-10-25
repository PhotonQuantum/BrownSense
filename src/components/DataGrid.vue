<template>
  <v-container>
    <v-layout text-center wrap>
      <v-flex mb-5 xs12>
        <p>Device ID: {{ device }}</p>
        <line-chart
          styles="width: 800px; height: 600px; position: relative;"
          :chart-data="datacollection"
          :options="chart_options"
          v-if="loaded"
        ></line-chart>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import LineChart from "./LineChart.js";
import PouchDB from 'pouchdb-browser'
export default {
  data: () => ({
    loaded: false,
    datacollection: null,
    time_filter: -1,
    chart_options: {
      animation: {
        duration: 0 // general animation time
      },
      elements: {
        line: {
          tension: 0 // disables bezier curves
        }
      },
      scales: {
        xAxes: [
          {
            type: "time",
            time: {
              parser: "x"
            }
          }
        ]
      }
    },
  }),
  components: { LineChart },
  props: ["device"],

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
   datagrid() {
     return {
       database: this.db_datagrid,
       selector: {
         device: this.device,
         type: "h2s",
         time: { $gt: this.time_filter - 1000 }
       },
       sort: [{ time: "asc" }]
     }
   }
  },
  watch: {
    datagrid: function(val) {
      var filter_time;
      filter_time = new Date() / 1000 - 500;
      console.log(filter_time);
      this.datacollection = {
        // labels: ["H2S"],
        datasets: [
          {
            label: "H2S",
            backgroundColor: "#f87979",
            data: val.filter(x => x.time > filter_time).map(x => ({ x: x.time * 1000, y: x.data }))
          }
        ]
      };
    }
  },

  created: function() {
    this.loaded = false;
    this.time_filter = new Date()/1000;
    // Send all documents to the remote database, and stream changes in real-time. Note if you use filters you need to set them correctly for pouchdb and couchdb. You can set them for each direction separatly: options.push/options.pull. PouchDB might not need the same filter to push documents as couchdb to send the filtered requested documents.
    /*
    this.$pouch.pull("datagrid", "http://localhost:5984/datagrid", {
      ...{ selector: this.db_selector },
      ...{ live: true }
    });
    */
   this.db_datagrid = new PouchDB("http://localhost:5984/datagrid")
    // this.$pouch.sync("dev_one", "http://localhost:5984/test");
    this.$on("pouchdb-db-created", function() {
      this.loaded = true;
    });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
