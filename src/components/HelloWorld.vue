<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div v-if="loaded" class="small">
      <line-chart
        styles="width: 800px; height: 600px; position: relative;"
        :chart-data="datacollection"
        :options="chart_options"
      ></line-chart>
    </div>
    <p>
      For a guide and recipes on how to configure / customize this project,
      <br />check out the
      <a
        href="https://cli.vuejs.org"
        target="_blank"
        rel="noopener"
      >vue-cli documentation</a>.
    </p>
    <h3>Installed CLI Plugins</h3>
    <ul>
      <li>
        <a
          href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-babel"
          target="_blank"
          rel="noopener"
        >babel</a>
      </li>
      <li>
        <a
          href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-eslint"
          target="_blank"
          rel="noopener"
        >eslint</a>
      </li>
    </ul>
    <h3>Essential Links</h3>
    <ul>
      <li>
        <a href="https://vuejs.org" target="_blank" rel="noopener">Core Docs</a>
      </li>
      <li>
        <a href="https://forum.vuejs.org" target="_blank" rel="noopener">Forum</a>
      </li>
      <li>
        <a href="https://chat.vuejs.org" target="_blank" rel="noopener">Community Chat</a>
      </li>
      <li>
        <a href="https://twitter.com/vuejs" target="_blank" rel="noopener">Twitter</a>
      </li>
      <li>
        <a href="https://news.vuejs.org" target="_blank" rel="noopener">News</a>
      </li>
    </ul>
    <h3>Ecosystem</h3>
    <ul>
      <li>
        <a href="https://router.vuejs.org" target="_blank" rel="noopener">vue-router</a>
      </li>
      <li>
        <a href="https://vuex.vuejs.org" target="_blank" rel="noopener">vuex</a>
      </li>
      <li>
        <a
          href="https://github.com/vuejs/vue-devtools#vue-devtools"
          target="_blank"
          rel="noopener"
        >vue-devtools</a>
      </li>
      <li>
        <a href="https://vue-loader.vuejs.org" target="_blank" rel="noopener">vue-loader</a>
      </li>
      <li>
        <a href="https://github.com/vuejs/awesome-vue" target="_blank" rel="noopener">awesome-vue</a>
      </li>
    </ul>
  </div>
</template>

<script>
import LineChart from "./LineChart.js";
export default {
  name: "HelloWorld",
  components: { LineChart },
  data: () => ({
    loaded: false,
    datacollection: null,
    datenow: 999999999,
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
              parser: "X"
            }
          }
        ]
      }
    }
  }),
  methods: {
    update_time() {
      this.datenow = new Date() / 1000;
    }
  },

  pouch: {
    dev_one() {
      return {
        database: "datagrid",
        selector: {
          device: "1",
          type: "h2s",
          time: { $gt: this.datenow - 100 }
        },
        sort: [{time: "asc"}]
      };
    }
  },
  /*
  computed: {
    datacollection: function() {
      return {
        // labels: ["H2S"],
        datasets: [
          {
            label: "H2S",
            backgroundColor: "#f87979",
            data: this.dev_one.map(x => ({ x: x.time, y: x.info }))
          }
        ]
      };
    }
  },
  */
  watch: {
    dev_one: function(val) {
      this.datacollection = {
        // labels: ["H2S"],
        datasets: [
          {
            label: "H2S",
            backgroundColor: "#f87979",
            data: val.map(x => ({ x: x.time, y: x.data }))
          }
        ]
      };
    }
  },
  props: {
    msg: String
  },

  created: function() {
    this.loaded = false;
    // Send all documents to the remote database, and stream changes in real-time. Note if you use filters you need to set them correctly for pouchdb and couchdb. You can set them for each direction separatly: options.push/options.pull. PouchDB might not need the same filter to push documents as couchdb to send the filtered requested documents.
    this.$pouch.sync("datagrid", "http://localhost:5984/datagrid");
    // this.$pouch.sync("dev_one", "http://localhost:5984/test");
    this.$on("pouchdb-db-created", function() {
      this.loaded = true;
    });
  },
  mounted: function() {
    setInterval(this.update_time, 1000);
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